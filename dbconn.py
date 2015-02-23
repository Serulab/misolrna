

class TempTables(object):
    
    def __init__(self,dbname):
        """ init DB """
        import sqlite3
        self._conn = sqlite3.connect(dbname)
        c = self._conn.cursor()
        c.execute("CREATE TEMP TABLE kk(codigobin TEXT)")
        
    def get_parIDs(self,allbins):
        c = self._conn.cursor()
        for x in allbins:
            c.execute("INSERT INTO kk values (?)",(x,))
        #c.execute("CREATE TEMP TABLE kk2 as SELECT parID FROM parid_bin WHERE bin in (SELECT codigobin from kk)")
        c.execute("CREATE TEMP TABLE kk2 as SELECT parid_bin.parID as parID FROM parid_bin INNER JOIN kk ON parid_bin.bin = kk.codigobin")
        #c.execute("SELECT parID FROM parid_bin WHERE bin in (SELECT codigobin from kk)")
        # ver si lo que sigue no lo puedo reemplazar por * de kk2!
        c.execute("SELECT parid_bin.parID FROM parid_bin INNER JOIN kk ON parid_bin.bin = kk.codigobin")
        return c

    def all_miranda_parID(self):
        c = self._conn.cursor()
        #c.execute("SELECT * FROM miranda WHERE parID in (SELECT parID from kk2)")
        c.execute("SELECT m.* FROM miranda m INNER JOIN kk2 ON (m.parID = kk2.parID)")
        return c.fetchall()
        
    def par_ID_from_keys(self, keywords):        
        c = self._conn.cursor()
        c.execute("SELECT parID FROM miranda WHERE unigenes_desc LIKE :keys",{'keys':'%'+keywords+'%'})
        return c.fetchall()

    def create_kk3(self,parid_diff):
        c = self._conn.cursor()
        c.execute("CREATE TEMP TABLE kk3(codigo_parid TEXT)")
        for x in parid_diff:
            c.execute("INSERT INTO kk3 values (?)",(x,))
        #c.execute("SELECT * FROM miranda WHERE parid in (SELECT codigo_parid from kk3)")
        c.execute("SELECT m.* FROM miranda m INNER JOIN kk3 ON (m.parid = kk3.codigo_parid)")
        return c

    def close(self):
        """cierra DB"""
        self._conn.close()


class DBInterac(object):
    
    def __init__(self,dbname):
        """ Inicializa DB """
        import sqlite3
        self._conn = sqlite3.connect(dbname)
        
    def close(self):
        """cierra DB"""
        self._conn.close()
        
    def pubids(self, mirna_id):
        c = self._conn.cursor()
        c.execute("SELECT pub_id FROM mirna_pubs WHERE ID = ?;",(mirna_id,))
        return c.fetchall()
        
    def aid(self,pub_id):
        c = self._conn.cursor()
        c.execute('SELECT a_ID FROM articles_authors WHERE pub_id = ?',pub_id)
        return c.fetchall()
        
    def authorname(self,autor_id):
        c = self._conn.cursor()
        c.execute('SELECT name FROM authors WHERE rowid = ?',(autor_id,))
        return c.fetchone()[0]

    def articles(self,pub_id):
        c = self._conn.cursor()
        c.execute("SELECT * FROM articles WHERE rowid = ?;",pub_id)
        return c.fetchone()

    def journals(self,pub_name):
        c = self._conn.cursor()
        c.execute('SELECT name FROM journals WHERE rowid = ?',(pub_name[1],))
        return c.fetchone()[0]
        
    def met_qtl(self,bin_):
        c = self._conn.cursor()
        c.execute('SELECT metabolites,QTL FROM bins WHERE bin = ?',(bin_,))
        return c.fetchone()
        
    def datafrom_precu_blast_ali(self,r_name,mirna,r_ini):
        c = self._conn.cursor()
        c.execute('SELECT queryname, e, iden, bits, query, alignname, match, sbjct FROM precu_blast WHERE (r_name = ? AND alignname = ? AND r_ini = ?)',(r_name,mirna,r_ini))
        return c.fetchall()
        
    def datafrom_precu_blast_micro(self,r_name,mirna,r_ini):
        c = self._conn.cursor()
        c.execute('SELECT queryname, e, iden, bits, query, alignname, match, sbjct FROM precu_blast WHERE (r_name = ? AND micro = ? AND r_ini = ?)',(r_name,mirna,r_ini))
        return c.fetchall()
        
    def r_miranda(self,mirna):
        c = self._conn.cursor()
        c.execute("SELECT * FROM miranda WHERE q_name = ?;",(mirna,))
        return c.fetchall()
        
    def seq_from_mirnas(self,mirna):
        c = self._conn.cursor()
        c.execute("SELECT seq FROM mirnas WHERE ID = ?;",(mirna,))
        return c.fetchone()[0]
        
    def bin_from_parid(self,parID):
        c = self._conn.cursor()
        c.execute('SELECT bin FROM parid_bin WHERE parID =?',(parID,))
        return c.fetchone()

    def miranda_rname(self,target):
        c = self._conn.cursor()
        c.execute("SELECT * FROM miranda WHERE r_name = ?;",(target,))
        return c.fetchall()
        
    def bac_unigenesbacs_target(self,target):
        c = self._conn.cursor()
        c.execute("SELECT bac FROM unigene_bacs WHERE target = ?;",(target,))
        return c.fetchall()
        
    def markerid_bacmarkers_bacs(self,tmp):
        c = self._conn.cursor()
        c.execute("SELECT marker_id FROM bacs_markers WHERE bacs = ?;",tmp)
        return c.fetchall()
        
    def mcp_markers_markerid(self,markid):
        c = self._conn.cursor()
        c.execute("SELECT map,crm,position FROM markers WHERE marker_id = ?;",markid)
        return c.fetchone()
        
    def bin1(self,bin_):
        c = self._conn.cursor()
        #c.execute("SELECT * FROM miranda WHERE parID in (SELECT parID FROM parid_bin WHERE bin = ?)",(bin_,))
        c.execute("SELECT m.* FROM miranda m INNER JOIN parid_bin pb ON (m.parID = pb.parID AND pb.bin = ?)",(bin_,)) 
        return c.fetchall()

    def count_align(self,mirna):
        c = self._conn.cursor()
        c.execute('SELECT COUNT(*) FROM precu_blast WHERE alignname = ?',(mirna,))
        return int(c.fetchone()[0])
    
    def bin_from_bins_qtl(self,keywords):
        c = self._conn.cursor()
        c.execute("SELECT bin FROM bins WHERE qtl LIKE :keys",{'keys':'%'+keywords+'%'})
        return c.fetchall()

    def parID_from_target(self,target):
        c = self._conn.cursor()
        c.execute("SELECT parID FROM miranda WHERE r_name = ?",(target,))
        return c.fetchone()
    
    def bin_from_bins_metab(self,keywords):
        c = self._conn.cursor()
        c.execute("SELECT bin FROM bins WHERE metabolites LIKE :keys",{'keys':'%'+keywords+'%'})
        return c
