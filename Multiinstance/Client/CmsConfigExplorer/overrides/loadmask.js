Ext.override(Ext.LoadMask, {
    getStoreListeners: function(store) {
        var load = this.onLoad,
            beforeLoad = this.onBeforeLoad,
            result = {
                // Fired when a range is requested for rendering that is not in the cache
                cachemiss: beforeLoad,

                // Fired when a range for rendering which was previously missing from the cache is loaded
                cachefilled: load
            };

        // Only need to mask on load if the proxy is asynchronous - ie: Ajax/JsonP
        if (!store.proxy.isSynchronous) {
            result.beforeload = beforeLoad;
            result.load = load;
        }
        return result;
    }
});