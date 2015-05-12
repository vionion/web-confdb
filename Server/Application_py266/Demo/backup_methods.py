#Get a configuration 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def conf(self):
        db = cherrypy.request.db
#        ver = db.query(Version).get(length)
        ver = db.query(Version).all()
        for v in ver:
            print v.id, v.name
        #output = """<html><head></head><body> Title: <br>"""
        #output = output + str(ver.id)+" "+ver.name
            
        #for p2c in db.query(Pathidconf).filter(Pathidconf.id_confver == ver.id).all():
        #    pid = db.query(Pathids).filter(Pathids.id == p2c.id_pathid).one()
        #    spa = db.query(Paths).filter(Paths.id == pid.id_path).one()
        #    output = output+"<br>"+spa.name+" "+str(pid.id)
                #print spa.name
#        schema = PathsSchema(many=True)
#        pats = db.query(Paths).from_statement(text("SELECT u_paths.id, u_paths.name "
#						+ "FROM u_paths, u_pathid2conf, u_pathids "
#						+ "WHERE u_pathids.id = u_pathid2conf.id_pathid "
#						+ "AND u_pathids.id_path = u_paths.id AND u_pathid2conf.id_confver=:idv AND u_pathids.isEndPath = 0 order by u_pathid2conf.ord")).params(idv=length).all()
            #output = output+"<br>"+pat.name
        
        output = schema.dump(pats)
        #output = output + """</body> </html>""" 
        return output.data
    
    #Get a the list of paths from configuration 
    @cherrypy.expose
#    @cherrypy.tools.json_out()
    def fullsequence(self):
        db = cherrypy.request.db
        num = db.query(Pathitems.id_pae).from_statement(text("SELECT u_pathid2pae.id_pae FROM u_pathid2pae WHERE u_pathid2pae.id = 798")).first()
        pats = db.query(Pathitems).filter(Pathitems.id_parent.in_(num)).all()
#        
#        from_statement(text("SELECT u_pathid2pae.id, u_pathid2pae.id_pathid, u_pathid2pae.id_pae, u_pathid2pae.id_parent, u_pathid2pae.lvl "
##						+ "DECODE(u_paelements.paetype,1, 'mod', 2, 'seq', 3, 'oum', 'Undefined') "
#                        + "FROM u_pathid2pae, u_paelements "
##						+ "AS entry_type, u_pathid2pae.operator "
##						+ "WHERE u_pathid2pae.lvl>1 "
#						+ "WHERE u_pathid2pae.id_parent IN (SELECT u_paelements.id FROM u_paelements, u_pathid2pae WHERE u_paelements.id = u_pathid2pae.id_pae AND u_pathid2pae.id = 798)")).all()
#						+ "ORDER BY u_pathid2pae.ord")).all()
        print "RSULTS", num[0], len(pats)
        for p in pats:
            print p.id, p.id_pathid, p.id_pae, p.id_parent, p.lvl
            
#        ver = db.query(Version).from_statement(text("SELECT u_confversions.id "
##						+ "DECODE(u_paelements.paetype,1, 'mod', 2, 'seq', 3, 'oum', 'Undefined') "
#                        + "FROM u_confversions, u_pathid2conf "
##						+ "AS entry_type, u_pathid2pae.operator "
#						+ "WHERE u_pathid2conf.id_pathid=5")).all()
#        for v in ver:
#            print v.id      
        return num
    
    #Get a the list of paths from configuration 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def paths(self, _dc=101, length=1):
        db = cherrypy.request.db
        resp = Response()
        schema = ResponsePathsSchema()
        pats = db.query(Paths).from_statement(text("SELECT u_paths.id, u_paths.name "
						+ "FROM u_paths, u_pathid2conf, u_pathids "
						+ "WHERE u_pathids.id = u_pathid2conf.id_pathid "
						+ "AND u_pathids.id_path = u_paths.id AND u_pathid2conf.id_confver=:idv AND u_pathids.isEndPath = 0 order by u_pathid2conf.ord")).params(idv=length).all()
            #output = output+"<br>"+pat.name
        resp.success = True
        resp.data = pats
        
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)
        
        #output = output + """</body> </html>""" 
        return output.data
    
#Get a the list of pathitems from configuration 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def treepaths(self, _dc=101, length=1, node="", itype="", idpae=0, idpath=0):
        db = cherrypy.request.db
        schema = None
        #Query for the level 0 items of the Path
        if(itype == 'pat'):
            resp = ResponseTree()
            schema = ResponsePathItemsSchema()
            
#            subquery = select([Pathitems.id_pae]).where(and_(Pathitems.id_pathid == node, Pathitems.lvl == 0))
#            exists().where(and_(Pathitems.id_pathid == node, Pathitems.lvl == 0, Pathelement.id == Pathitems.id_pae))
#            pialias = aliased(Pathitems, subquery)
#            
#            pals = db.query(Pathelement).join(Pathelement.id == pialias.id_pae).all()
#        filter(Pathelement.id == subquery.c.id_pae).order_by(Pathelement.ord).all()
            
            lista = db.query(Pathitems).filter(Pathitems.id_pathid == node).filter(Pathitems.lvl == 0).all()
            
#            for p in lista:
#                print p.id_pae, p.id, p.id_pathid
             
#            result = db.query(Pathelement.id, Pathelement.name, Pathelement.paetype).filter(Pathelement.id==2).one()
#            print result
#            print lista
            newlista = []
            pals = []
            for p in lista:
                newlista.append(p.id_pae)
                res = db.query(Pathelement).from_statement(text("SELECT u_paelements.id, u_paelements.name, u_paelements.paetype FROM u_paelements WHERE u_paelements.id=:param1")).params(param1=p.id_pae).one()
#                .id, Pathelement.name, Pathelement.paetype).filter(Pathelement.id==p.id_pae)
                pals.append(res)
#                print res.id
#        
#            print pals
#            
##            pals = db.query(Pathelement).filter(Pathelement.id.in_(newlista)).all()
#            
#            for p in pals:
#                print p.id, p.name
            
#            pats = db.query(Pathitems.id_pae).from_statement(text("SELECT u_pathid2pae.id_pae " #u_pathid2pae.id, u_pathid2pae.id_pathid, 
##						+ "DECODE(u_paelements.paetype,1, 'mod', 2, 'seq', 3, 'oum', 'Undefined') "
#                        + "FROM u_pathid2pae, u_pathid2conf "
##						+ "AS entry_type, u_pathid2pae.operator "
#						+ "WHERE u_pathid2pae.id_pathid=:node "
#						+ "AND u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
#						+ "and u_pathid2pae.lvl=0 "
#						+ "AND u_pathid2conf.id_confver=:idv "
#						+ "ORDER BY u_pathid2pae.ord")).params(idv=length, node=node).all()
#            
#            pals = db.query(Pathelement).filter(Pathelement.id.in_(pats)).all()
            
#            pals = db.query(Pathelement).from_statement(text("SELECT u_paelements.id, u_paelements.name, u_paelements.paetype FROM u_paelements, u_pathid2pae WHERE u_paelements.id IN "
#                        + "(SELECT u_pathid2pae.id_pae "
#                        + "FROM u_pathid2pae, u_pathid2conf "
#						+ "WHERE u_pathid2pae.id_pathid=:node "
#						+ "AND u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
#						+ "and u_pathid2pae.lvl=0 "
#						+ "AND u_pathid2conf.id_confver=:idv "
#						+ ")")).params(idv=length, node=node).all() #ORDER BY u_pathid2pae.ord
            
            resp.children = pals
        #Query for the level 0 items of the Sequence
        elif(itype == 'seq'):
            resp = ResponseTree()
            schema = ResponsePathItemsSchema()
#            pats = db.query(Pathelement).filter(Pathelement.id_parent == idpae).order_by(Pathelement.ord).all() #filter(Pathitems.id_pathid == idpath).
#           
            lista = db.query(Pathitems.id_pae).filter(Pathitems.id_parent == node).filter(Pathitems.lvl > 0).order_by(Pathitems.order).all()
            pats = []
            for l in lista:
                res = db.query(Pathelement).from_statement(text("SELECT u_paelements.id, u_paelements.name, u_paelements.paetype "
                            + "FROM u_paelements "
                            + "WHERE u_paelements.id=:node ")).params(node=l.id_pae).one()
                pats.append(res)
            resp.children = pats
        
        else:
            resp = ResponseTree()
            schema = ResponsePathTreeSchema()
            pats = db.query(Pathids).from_statement(text("SELECT u_pathids.id, u_pathids.id_path "
						  + "FROM  u_pathids, u_pathid2conf "
						  + "WHERE u_pathids.id = u_pathid2conf.id_pathid "
						  + "AND u_pathid2conf.id_confver=:idv AND u_pathids.isEndPath = 0 order by u_pathid2conf.ord")).params(idv=length).all()
            #output = output+"<br>"+pat.name
            resp.children = pats
           
        resp.success = True
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)
        
        #output = output + """</body> </html>""" 
        return output.data
    
    #Get a the list of pathitems from a path
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pathitems(self, _dc=101, length=53, node=450):
        db = cherrypy.request.db
        resp = ResponseTree()
        schema = ResponsePathItemsSchema()
        pats = db.query(Pathitems).from_statement(text("SELECT u_paelements.id, u_paelements.name, u_pathid2pae.id_parent "
#						+ "DECODE(u_paelements.paetype,1, 'mod', 2, 'seq', 3, 'oum', 'Undefined') "
                        + "FROM u_paelements, u_pathid2pae "
#						+ "AS entry_type, u_pathid2pae.operator "
						+ "WHERE u_pathid2pae.id_pathid=:node "
						+ "AND u_pathid2pae.id_pae=u_paelements.id "
#						+ "and u_pathid2pae.lvl=0 "
#						+ "AND u_pathid2conf.id_confver=:idv "
						+ "ORDER BY u_pathid2pae.ord")).params(idv=length, node=node).all()
            #output = output+"<br>"+pat.name
        resp.success = True
        resp.children = pats
        
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)
        
        #output = output + """</body> </html>""" 
        return output.data
    
    
    #Get the modules of a given path 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allmodules(self, _dc=101,length=53, pat=5249):
        resp = Response()
        db = cherrypy.request.db
        #ver = db.query(Version).get(length)
        #print ver.id
        #print ver.name
        #print ver.id_release
        #output = """<html><head></head><body> Title: <br>"""
        #output = output + str(ver.id)+" "+ver.name  
        #for p2c in db.query(Pathidconf).filter(Pathidconf.id_confver == ver.id).all():
        #    pid = db.query(Pathids).filter(Pathids.id == p2c.id_pathid).one()
        #    spa = db.query(Paths).filter(Paths.id == pid.id_path).one()
        #    output = output+"<br>"+spa.name
        #schema = ModuleSchema(many=True)
        schema = ResponseSchema()
        mods = db.query(Module).from_statement(text("SELECT u_paelements.id, u_paelements.name "                      
						+ "FROM u_paelements, u_pathid2pae, u_pathid2conf "
						+ "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "                          
						+ "AND u_pathid2pae.id_pae=u_paelements.id "
						+ "AND u_paelements.paetype=:one "
                        + "AND u_pathid2conf.id_pathid IN (SELECT u_pathid2conf.id_pathid FROM u_pathid2conf WHERE u_pathid2conf.id_confver=:idv) "
						#+ "and u_mod2templ.id_pae=u_paelements.id "
						+ "AND u_pathid2conf.id_confver=:idv order by u_paelements.name")).params(idv=length, pa=pat, one=1).all()
            #output = output+"<br>"+mod.name
            #print mod.name
        #print "out for"
        resp.success = True
        resp.data = mods
        
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)
        
        #output = output + """</body> </html>""" 
        return output.data
    
    #Get the modules of a given path 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def modules(self, _dc=101,length=53, pat=5249):
        resp = Response()
        db = cherrypy.request.db
        #ver = db.query(Version).get(length)
        #print ver.id
        #print ver.name
        #print ver.id_release
        #output = """<html><head></head><body> Title: <br>"""
        #output = output + str(ver.id)+" "+ver.name  
        #for p2c in db.query(Pathidconf).filter(Pathidconf.id_confver == ver.id).all():
        #    pid = db.query(Pathids).filter(Pathids.id == p2c.id_pathid).one()
        #    spa = db.query(Paths).filter(Paths.id == pid.id_path).one()
        #    output = output+"<br>"+spa.name
        #schema = ModuleSchema(many=True)
        schema = ResponseSchema()
        mods = db.query(Module).from_statement(text("SELECT u_paelements.id, u_paelements.name "
						+ "FROM u_paelements, u_pathid2pae, u_pathid2conf "                        
						+ "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
						+ "AND u_pathid2pae.id_pae=u_paelements.id "
						+ "AND u_paelements.paetype=:one "
                        + "AND u_pathid2conf.id_pathid=:pa "
						#+ "and u_mod2templ.id_pae=u_paelements.id "
						+ "AND u_pathid2conf.id_confver=:idv order by u_paelements.name")).params(idv=length, pa=pat, one=1).all()
            #output = output+"<br>"+mod.name
            #print mod.name
        #print "out for"
        resp.success = True
        resp.data = mods
        
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)
        
        #output = output + """</body> </html>""" 
        return output.data    
    
    
    
    #Get the parameters of a given module                                                   
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def modparams(self, _dc=233, id=17009):
        resp = Response()
        db = cherrypy.request.db
        
        schema = ResponseParamsSchema()
        parameters = db.query(Modelement).from_statement(text("SELECT u_moelements.id, u_moelements.name, u_moelements.paramtype, u_moelements.value "
						+ "FROM u_moelements, u_pae2moe "
						+ "WHERE u_moelements.id = u_pae2moe.id_moe "
                        + "AND u_moelements.moetype=:one "                                     
						+ "AND u_pae2moe.id_pae=:idm "
						+ "order by u_pae2moe.ord")).params(idm=id, one=1).all()

        resp.success = True
        resp.data = parameters
        
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)
        
        #output = output + """</body> </html>""" 
        return output.data
    
    #______________________________________________
    
    
    
    #Get the directories of the DB                                                   
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def directories(self,_dc=101, node = ""):
        db = cherrypy.request.db
        
        resp = Response()
        schema = ResponseFolderitemSchema()
        
        node= int(node) 
        
        folder_items_dict ={}
        
        if(node !=-1):   
        
            #finding Root
            fRoot = db.query(Directory).filter(Directory.name == "/").first()
            if (fRoot == None):
                print "NO ROOT!!!!!!"
    #        rootItem = FolderItem(fRoot.id, fRoot.name, "fol",fRoot.id_parentdir, fRoot.created) 
    #        rootItem.gid = self.folMap.put(self.idfolgen,rootItem)
        
            #find Root Children
#            directories = db.query(Directory).all()   
            directories = db.query(Directory).filter(Directory.id == fRoot.id).all()

            for d in directories:
                f = FolderItem(d.id, d.name, "fol",d.id_parentdir, d.created)    
                f.gid = self.folMap.put(self.idfolgen,f)

    #            configs = db.query(Configuration).from_statement(text("SELECT DISTINCT u_configurations.id, u_configurations.name FROM u_configurations JOIN u_confversions ON u_configurations.id = u_confversions.id_config and u_confversions.id_parentdir=:id_par")).params(id_par=d.id).all()

                configs = db.query(Configuration).from_statement(text("SELECT  u_configurations.id, u_configurations.name FROM u_configurations, u_confversions WHERE u_configurations.id = u_confversions.id_config and u_confversions.id_parentdir=:id_par")).params(id_par=d.id).all()            

                if (len(configs) > 0):
                    print "THERE ARE CONFIGS"
                    for c in configs:
                        cnf = FolderItem(c.id, c.name, "cnf",d.id, None)
                        cnf.gid = self.cnfMap.put(self.idfolgen,cnf)
                        f.children.append(cnf)

                folder_items_dict[f.id] = f

            #Nesting folders
            folKeys = folder_items_dict.keys() #viewkeys()
            for fk in folKeys:
                if (not(fk == fRoot.id)):
                    fi = folder_items_dict.get(fk)
                    folder_items_dict.get(fi.id_parent).children.append(fi)
        
        else:
            myRoot = self.folMap.get(node)
            #finding Node Dir
            fRoot = db.query(Directory).filter(Directory.id == myRoot).first()
            if (fRoot == None):
                print "NO ROOT!!!!!!"
    #        rootItem = FolderItem(fRoot.id, fRoot.name, "fol",fRoot.id_parentdir, fRoot.created) 
    #        rootItem.gid = self.folMap.put(self.idfolgen,rootItem)
        
            #find Root Children
#            directories = db.query(Directory).all()   
            directories = db.query(Directory).filter(Directory.id == fRoot.id).all()

            for d in directories:
                f = FolderItem(d.id, d.name, "fol",d.id_parentdir, d.created)    
                f.gid = self.folMap.put(self.idfolgen,f)

    #            configs = db.query(Configuration).from_statement(text("SELECT DISTINCT u_configurations.id, u_configurations.name FROM u_configurations JOIN u_confversions ON u_configurations.id = u_confversions.id_config and u_confversions.id_parentdir=:id_par")).params(id_par=d.id).all()

                configs = db.query(Configuration).from_statement(text("SELECT  u_configurations.id, u_configurations.name FROM u_configurations, u_confversions WHERE u_configurations.id = u_confversions.id_config and u_confversions.id_parentdir=:id_par")).params(id_par=d.id).all()            

                if (len(configs) > 0):
                    print "THERE ARE CONFIGS"
                    for c in configs:
                        cnf = FolderItem(c.id, c.name, "cnf",d.id, None)
                        cnf.gid = self.cnfMap.put(self.idfolgen,cnf)
                        f.children.append(cnf)

                folder_items_dict[f.id] = f

            #Nesting folders
            folKeys = folder_items_dict.keys() #viewkeys()
            for fk in folKeys:
                if (not(fk == fRoot.id)):
                    fi = folder_items_dict.get(fk)
                    folder_items_dict.get(fi.id_parent).children.append(fi)
            

        #Append Root
        resp.success = True
        rootFol = folder_items_dict.get(fRoot.id)
        rootFol.expanded = True
        resp.children = []
        resp.children.append(rootFol)
        
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)

        return output.data
    
    #Check paelement 9240