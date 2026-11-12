# -*- coding: utf-8 -*-
from datetime import datetime, time, timedelta

import pytz

from odoo import _, api, fields, models
from odoo.exceptions import AccessError

SOLD_STATES = ('paid', 'done', 'invoiced')
PURCHASE_STATES = ('purchase', 'done')


class ShopDashboard(models.AbstractModel):
    """Data provider of the Script Shop Management dashboard (no table).

    A dashboard scope is a local shop (point of sale) or all the local shops. The hooks `_get_scope` and
    `_get_extra_data` let an extension module widen the scope and add indicators.
    """
    _name = 'shop.dashboard'
    _description = "Shop Dashboard"

    # ----------------------------------------------------------------------- access

    @api.model
    def _check_access_group(self):
        if not self.env.user.has_group('script_shop_management.group_shop_user'):
            raise AccessError(_("You are not allowed to access the shop dashboard."))

    @api.model
    def _get_shops(self):
        return self.env['pos.config'].search([('is_shop', '=', True)])

    # ------------------------------------------------------------------------ cards

    @api.model
    def get_shops(self):
        """Cards of the dashboard: all the shops, then each local shop."""
        self._check_access_group()
        company = self.env.company
        shops = self._get_shops()
        cards = [{
            'key': 'all',
            'id': False,
            'website_id': False,
            'name': _("All shops"),
            'image_url': f'/web/image/res.company/{company.id}/logo',
            'shop_count': len(shops),
        }]
        for shop in shops:
            cards.append({
                'key': f'shop_{shop.id}',
                'id': shop.id,
                'website_id': False,
                'name': shop.name,
                'image_url': f'/web/image/pos.config/{shop.id}/shop_image?unique={shop.write_date.timestamp()}'
                             if shop.shop_image else '/web/static/img/placeholder.png',
                'shop_count': 1,
                'local': True,
                'online': False,
            })
        return cards

    # ------------------------------------------------------------------------- data

    @api.model
    def _to_utc(self, day, end=False):
        """Convert a local date (YYYY-MM-DD) to a naive UTC datetime, in the user's timezone."""
        tz = pytz.timezone(self.env.user.tz or 'UTC')
        day = fields.Date.from_string(day)
        local = tz.localize(datetime.combine(day + timedelta(days=1 if end else 0), time.min))
        return local.astimezone(pytz.utc).replace(tzinfo=None)

    @api.model
    def _get_scope(self, shop_id, website_id=False):
        """Records the indicators are computed on."""
        shops = self.env['pos.config'].browse(shop_id) if shop_id else self._get_shops()
        return {'shops': shops}

    @api.model
    def get_data(self, shop_id, date_from, date_to, website_id=False):
        """Indicators of a local shop, or of all the local shops."""
        self._check_access_group()
        scope = self._get_scope(shop_id, website_id)
        scope.update(start=self._to_utc(date_from), end=self._to_utc(date_to, end=True))
        data = {
            'currency_id': self.env.company.currency_id.id,
            'purchases': self._get_purchases(**scope),
            'sales': self._get_sales(**scope),
            'stock': self._get_stock(**scope),
        }
        data.update(self._get_extra_data(shop_id=shop_id, website_id=website_id, **scope))
        return data

    @api.model
    def _get_extra_data(self, **scope):
        """Hook: indicators added by the extension modules."""
        return {}

    # ----------------------------------------------------------------------- sales

    @api.model
    def _get_sold_orders(self, shops, start, end):
        return self.env['pos.order'].search([
            ('config_id', 'in', shops.ids),
            ('state', 'in', SOLD_STATES),
            ('date_order', '>=', start),
            ('date_order', '<', end),
        ])

    @api.model
    def _get_sales(self, shops, start, end, **kw):
        """Sales of the local shops (point of sale orders, refunds counted as negative orders)."""
        orders = self._get_sold_orders(shops, start, end)
        refunds = orders.filtered('is_refund')
        return {
            'count': len(orders) - len(refunds),
            'refund_count': len(refunds),
            'amount': sum(orders.mapped('amount_total')),
        }

    # -------------------------------------------------------------------- purchases

    @api.model
    def _get_purchase_shop_domain(self, shops, **kw):
        return [('shop_id', 'in', shops.ids)]

    @api.model
    def _get_purchase_orders(self, shops, start, end, **kw):
        domain = [
            ('state', 'in', PURCHASE_STATES),
            ('date_approve', '>=', start),
            ('date_approve', '<', end),
            *self._get_purchase_shop_domain(shops, **kw),
        ]
        return self.env['purchase.order'].search(domain)

    @api.model
    def _get_purchases(self, shops, start, end, **kw):
        orders = self._get_purchase_orders(shops, start, end, **kw)
        return {'count': len(orders), 'amount': sum(orders.mapped('amount_total'))}

    # ------------------------------------------------------------------------ stock

    @api.model
    def _get_warehouses(self, shops, **kw):
        return shops.picking_type_id.warehouse_id

    @api.model
    def _get_received_shop_domain(self, shops, **kw):
        return [('shop_id', 'in', shops.ids)]

    @api.model
    def _get_stock(self, shops, start, end, **kw):
        locations = self._get_warehouses(shops, **kw).lot_stock_id
        quants = self.env['stock.quant'].search([('location_id', 'child_of', locations.ids)]) if locations else \
            self.env['stock.quant']
        received = self.env['stock.picking'].search_count([
            ('state', '=', 'done'),
            ('date_done', '>=', start),
            ('date_done', '<', end),
            ('picking_type_code', '=', 'incoming'),  # receipts only, not the deliveries to the customers
            *self._get_received_shop_domain(shops, **kw),
        ])
        return {
            'quantity': sum(quants.mapped('quantity')),
            'value': sum(q.quantity * q.product_id.standard_price for q in quants),
            'received_transfers': received,
        }
