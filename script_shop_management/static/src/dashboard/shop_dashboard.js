import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { formatMonetary } from "@web/views/fields/formatters";
import { standardActionServiceProps } from "@web/webclient/actions/action_service";

const { DateTime } = luxon;

export class ShopDashboard extends Component {
    static template = "script_shop_management.ShopDashboard";
    static props = { ...standardActionServiceProps };

    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.periods = [
            { key: "today", label: _t("Today") },
            { key: "week", label: _t("This week") },
            { key: "month", label: _t("This month") },
            { key: "year", label: _t("This year") },
            { key: "custom", label: _t("Custom") },
        ];
        this.state = useState({
            shops: [],
            shop: null, // selected card, null while the cards are displayed
            period: "month",
            dateFrom: "",
            dateTo: "",
            data: null,
            loading: false,
        });
        onWillStart(async () => {
            this.state.shops = await this.orm.call("shop.dashboard", "get_shops", []);
        });
    }

    // ------------------------------------------------------------------ navigation

    async openShop(shop) {
        this.state.shop = shop;
        await this.selectPeriod(this.state.period);
    }

    backToShops() {
        this.state.shop = null;
        this.state.data = null;
    }

    async selectPeriod(key) {
        this.state.period = key;
        const today = DateTime.local().startOf("day");
        const ranges = {
            today: [today, today],
            week: [today.startOf("week"), today.endOf("week").startOf("day")],
            month: [today.startOf("month"), today.endOf("month").startOf("day")],
            year: [today.startOf("year"), today.endOf("year").startOf("day")],
        };
        if (ranges[key]) {
            this.state.dateFrom = ranges[key][0].toISODate();
            this.state.dateTo = ranges[key][1].toISODate();
        }
        if (key !== "custom" || (this.state.dateFrom && this.state.dateTo)) {
            await this.loadData();
        }
    }

    async onDateChange(field, ev) {
        this.state[field] = ev.target.value;
        this.state.period = "custom";
        if (this.state.dateFrom && this.state.dateTo) {
            await this.loadData();
        }
    }

    async loadData() {
        this.state.loading = true;
        try {
            this.state.data = await this.orm.call("shop.dashboard", "get_data", [
                this.state.shop.id,
                this.state.dateFrom,
                this.state.dateTo,
                this.state.shop.website_id,
            ]);
        } finally {
            this.state.loading = false;
        }
    }

    money(value) {
        return formatMonetary(value, { currencyId: this.state.data.currency_id });
    }

    /** The "all shops" card: no single shop nor online shop selected. */
    get isAllShops() {
        return !this.state.shop.id && !this.state.shop.website_id;
    }

    /**
     * Open a list filtered on the selected shop.
     * `xmlid` is an action of this module, or a full "module.xmlid" of another one.
     * `filters` adds search filters, like {filter_online: 1} for the online orders only.
     */
    openList(xmlid, searchField, websiteField, filters = {}) {
        const shop = this.state.shop;
        let context = {};
        if (shop.website_id) {
            if (!websiteField) {
                return; // this list cannot be filtered on an online shop
            }
            context = { [`search_default_${websiteField}`]: shop.website_id };
        } else if (shop.id) {
            context = { [`search_default_${searchField}`]: shop.id };
        }
        for (const [name, value] of Object.entries(filters)) {
            context[`search_default_${name}`] = value;
        }
        const action = xmlid.includes(".") ? xmlid : `script_shop_management.${xmlid}`;
        this.actionService.doAction(action, { additionalContext: context });
    }
}

registry.category("actions").add("script_shop_management.dashboard", ShopDashboard);
