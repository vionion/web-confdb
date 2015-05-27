
Ext.define("Demo110315.view.globalpset.GlobalPsetTree",{
    extend: "Ext.tree.Panel",
    
    alias: 'widget.gpsettree',
    reference: 'gpsetTree',
    
    controller: "globalpset-globalpsettree",

    bind:{
        // bind store to view model "modules" store
        store:'{gpsets}'
//        selection: '{selectedService}'
 
    },
    
    title: 'Global Parameter Sets',
    useArrows: true,
    columns: [
        {
            xtype: 'treecolumn',
            text: 'Name',
            flex: 2,
            dataIndex: 'name'
        },
        { 
            xtype: 'gridcolumn', 
            header: 'Tracked', 
            dataIndex: 'tracked',
            renderer: function(v, meta, rec) 
                                {   var  data = rec.getData(); 
                                    if (data.tracked == 1)
                                        {return "tracked"} 
                                    else {return "untracked"} 
                                }
        }
    ]
});
