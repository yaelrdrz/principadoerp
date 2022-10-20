/** @odoo-module **/

import LazyBarcodeCache from '@stock_barcode/lazy_barcode_cache';

import {patch} from 'web.utils';

patch(LazyBarcodeCache.prototype, 'bi_multi_barcode_for_product', {

    setCache(cacheData) {
        for (const model in cacheData) {
            const records = cacheData[model];
            // Adds the model's key in the cache's DB.
            if (!this.dbIdCache.hasOwnProperty(model)) {
                this.dbIdCache[model] = {};
            }
            if (!this.dbBarcodeCache.hasOwnProperty(model)) {
                this.dbBarcodeCache[model] = {};
            }
            // Adds the record in the cache.
            const barcodeField = this._getBarcodeField(model);
            for (const record of records) {
                this.dbIdCache[model][record.id] = record;
                if (barcodeField) {
                    const barcode = record[barcodeField];
                    if (!this.dbBarcodeCache[model][barcode]) {
                        this.dbBarcodeCache[model][barcode] = [];
                    }
                    if (!this.dbBarcodeCache[model][barcode].includes(record.id)) {
                        this.dbBarcodeCache[model][barcode].push(record.id);
                        if (this.nomenclature && this.nomenclature.is_gs1_nomenclature && this.gs1LengthsByModel[model]) {
                            this._setBarcodeInCacheForGS1(barcode, model, record);
                        }
                    }
                    if(model == 'product.product' && cacheData.hasOwnProperty('product.barcode')){
                        const br_records = cacheData['product.barcode'];
                        for (const br_record of br_records) {
                            if (!this.dbBarcodeCache[model][br_record.barcode]) {
                                this.dbBarcodeCache[model][br_record.barcode] = [];
                            }
                            if (!this.dbBarcodeCache[model][br_record.barcode].includes(br_record.product_id)) {
                                this.dbBarcodeCache[model][br_record.barcode].push(br_record.product_id);
                                if (this.nomenclature && this.nomenclature.is_gs1_nomenclature && this.gs1LengthsByModel[model]) {
                                    this._setBarcodeInCacheForGS1BR(br_record.barcode, model, br_record);
                                }
                            }
                        }
                    }
                }
            }
        }
    },

    _setBarcodeInCacheForGS1BR(barcode, model, record) {
        const length = this.gs1LengthsByModel[model];
        if (!barcode || barcode.length >= length || isNaN(Number(barcode))) {
            // Barcode already has the good length, or is too long or isn't
            // fully numerical (and so, it doesn't make sense to adapt it).
            return;
        }
        const paddedBarcode = barcode.padStart(length, '0');
        // Avoids to override or mix records if there is already a key for this
        // barcode (which means there is a conflict somewhere).
        if (!this.dbBarcodeCache[model][paddedBarcode]) {
            this.dbBarcodeCache[model][paddedBarcode] = [record.product_id];
        } else if (!this.dbBarcodeCache[model][paddedBarcode].includes(record.product_id)) {
            const previousRecordId = this.dbBarcodeCache[model][paddedBarcode][0];
            const previousRecord = this.getRecord(model, previousRecordId);
            console.log(
                `Conflict for barcode %c${paddedBarcode}%c:`, 'font-weight: bold', '',
                `it could refer for both ${record.product_id} and ${previousRecord.product_id}.`,
                `\nThe last one will be used but consider to edit those products barcode to avoid error due to ambiguities.`
            );
        }
    }

});