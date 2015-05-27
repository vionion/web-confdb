Ext.define('Demo110315.view.endpath.EndPathModuleDetailsController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.endpath-endpathmoduledetails',
    
    onEndModDetailsLoad: function(store, records, successful, operation, node, eOpts){
        
        var first = records[0];
        
        var name = this.lookupReference('endModDetailsName');
        var author = this.lookupReference('endModDetailsAuthor');
        var mclass = this.lookupReference('endModDetailsClass');
        var mtype = this.lookupReference('endModDetailsType');
        var stream = this.lookupReference('endModDetailsStream');
        
        stream.setText("");
        stream.disable();
        
        name.setValue( first.get('name') );
        author.setValue( first.get('author') );
        mclass.setValue( first.get('mclass') );
        mtype.setValue( first.get('mt')  );
    },
    
    onEndOumModDetailsLoad: function(store, records, successful, operation, node, eOpts){
        
        var first = records[0];
        
        var name = this.lookupReference('endModDetailsName');
        var author = this.lookupReference('endModDetailsAuthor');
        var mclass = this.lookupReference('endModDetailsClass');
        var mtype = this.lookupReference('endModDetailsType');
        var stream = this.lookupReference('endModDetailsStream');
        
        name.setValue( first.get('name') );
        author.setValue( first.get('author') );
        mclass.setValue( first.get('mclass') );
        mtype.setValue( first.get('mt')  );
        stream.setText( first.get('stream')  );
        
        stream.enable();
    },
    
    onEndDetLoaded: function(mid,pid){
        this.getViewModel().getStore('endmoddetails').load({params: {mid: mid, pid: pid}});
    },
    
    onEndOumDetLoaded: function(mid,pid){
        this.getViewModel().getStore('endoummoddetails').load({params: {mid: mid, pid: pid}});
    }
    
    
    
});
