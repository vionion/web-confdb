Ext.define('CmsConfigExplorer.view.service.PrescaleGrid', {
            extend: 'Ext.grid.Panel',
//            alias: 'widget.pregrid',
//            enableLocking: true,
            loadMask: true,
//            width: '100%',
//            height: '75%',
            scrollable: true,
            columnLines: true,
//            enableLocking: true,
//            columns:[],
            store: {},
//            reference: 'prescaleGrid',
            lockedGridConfig: {
                header: false,
                collapsible: true,
                width: 150,
                forceFit: true
            },
            columns: [
                    {
                        xtype: 'gridcolumn',
                        lockable: true,
//                        locked: true,
                        text: 'Path Name',
                        width: 150,
//                        flex: 1,
                        dataIndex: 'name'
                    }
                ]
//            initComponent: function() {
//            	var me = this;
//           
//                me.callParent();
//                
//                var newColumns = [
//                    { text: 'F1', dataIndex: 'f1', locked: true },
//                	{ text: 'F2', dataIndex: 'f2' } 
//                ];
//                
//                // =====================================
//                me.reconfigure(null, newColumns);
//                // =====================================
//        	}
        });
        