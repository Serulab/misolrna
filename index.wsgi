#!/usr/bin/env python

# LICENSE: AGPL 3.0. Sebastian Bassi

import logging
import sys
import os
import bottle

#logging.basicConfig(filename='/tmp/example.log',level=logging.DEBUG)
bottle.debug(True)
import argparse
#logging.debug('sys.path before: ' + str(sys.path))
sys.path.append(os.path.realpath(__file__))

my_dir = os.path.dirname(__file__)
sys.path.append(my_dir)

sys.path.append(os.path.join(my_dir, 'settings'))

#sys.path.append('settings')
#logging.debug('sys.path after: ' + str(sys.path))
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--settings', help='setting file',
                    required=False)
args = parser.parse_args()

is_server = False

if args.settings:
    try:
        #print args.settings
        sys.stderr.write('args.settings: ' + args.settings)
        settings = __import__(args.settings)
    except ImportError:
        print "Format of settings: local_mac (without path and without .py"
        exit()
else:
    # Assume ths is running in Apache server
    is_server = True
    settings = __import__('server')
    import site
    os.chdir(my_dir)
    site.addsitedir(settings.VENVS)

bottle.TEMPLATE_PATH.insert(0, os.path.join(my_dir, 'views'))

from tempfile import mkstemp
from bottle import route, run, static_file, get, post, request
from bottle import cheetah_view as view
from dbconn import TempTables, DBInterac
from index_template import index_template as it
from cStringIO import StringIO
from Bio.Blast.Applications import NcbiblastnCommandline as blastcli
from Bio.Blast import NCBIXML

import cPickle
import subprocess


BASE_URL = settings.BASE_URL
ROOT_DIR = settings.ROOT_DIR
DB_NAME = settings.DB_NAME
STATIC_ROOT = settings.STATIC_ROOT
STATIC_URL = settings.STATIC_URL
EXPRESSION_S = settings.EXPRESSION_S

@route('/')
@view('index')
def index():
    return {'type':'index',
            'STATIC_URL':STATIC_URL,}

@get('/search')
@view('search')
def search():
    return {'STATIC_URL':STATIC_URL, 
            'type' : 'search',
            'title' : 'Search miRNA'}

@route('/blast')
@view('blast')
def blast():
    return {'STATIC_URL' : STATIC_URL, 
            'type' : 'blast',
            'title' : 'BLAST'}

@route('/help')
@view('help')    
def help():
    return {'STATIC_URL' : STATIC_URL, 
            'type' : 'help',
            'title' : 'Help'}


@route('/about')
@view('about')
def about():
    return {'STATIC_URL':STATIC_URL, 
            'type' : 'about',
            'title' : 'About'}


@route('/static/css/<filename>')
def css_static(filename):
    return static_file(filename, root='%scss/'%STATIC_ROOT)

@route('/static/rss.xml')
def rss_static():
    return static_file('rss.xml', root=STATIC_ROOT)

@route('/static/fonts/<filename>')
def fonts_static(filename):
    return static_file(filename, root='%sfonts/'%STATIC_ROOT)

@route('/static/js/<filename>')
def js_static(filename):
    return static_file(filename, root='%sjs/'%STATIC_ROOT)  

@get('/static/imgs/<filename:re:.*\.png>')
def imagesall(filename):
    return static_file(filename, root='static/imgs/')    

@get('/static/imgs/aligns/<filename:re:.*\.png>')
def imagesal(filename):
    return static_file(filename, root='static/imgs/aligns/')

@get('/static/imgs/exp/<filename:re:.*\.png>')
def imagesexp(filename):
    return static_file(filename, root='static/imgs/exp/')

@get('/static/xls/<filename:re:.*\.(xls)>')
def xlsfiles(filename):
    return static_file(filename, root='static/xls/')    


def _carga_pubs(mirna):
    ''' trae data de pubicaciones '''
    conn = DBInterac(DB_NAME)
    pubsid = conn.pubids(mirna)
    publicaciones = []
    for pubid in pubsid:
        autoresid_l = [x[0] for x in conn.aid(pubid)]
        autores_l = []
        for autorid in autoresid_l:
            autores_l.append(conn.authorname(autorid))
        pubname = list(conn.articles(pubid))
        pubname[1] = conn.journals(pubname)
        publicaciones.append((pubname,autores_l))
    conn.close()
    return publicaciones
    
    
def _align_var(s,u,v,ancho):
    ''' Hace alineamiento en HTML '''
    ancho = 60
    divs = len(s)/ancho + 1
    out_s = ''
    for x in range(divs):
        init = x*ancho
        out_s+='<p class="dnaseq">'+s[init:init+ancho]+'<br/>'+u[init:init+ancho]+'<br/>'+\
        v[init:init+ancho]+'</p>'
    return out_s
    
def metayqtl(bin_):
    ''' busco metabolitos y QTL desde bin'''
    conn = DBInterac(DB_NAME)
    if '-' in bin_:
        # busco de a 1
        bin1 = bin_.split('-')[0]
        numero_bin = bin1[0] if len(bin1)==2 else bin1[:-1]
        #sacar parte numerica de bin1
        bin2_letra = bin_.split('-')[1]
        bin2 = numero_bin + bin2_letra
        metabolites_QTL_1 = conn.met_qtl(bin1)
        metabolites_QTL_2 = conn.met_qtl(bin2)
        if metabolites_QTL_1 and metabolites_QTL_2:
            metabolites1,QTL1 = metabolites_QTL_1
            metabolites2,QTL2 = metabolites_QTL_2
        elif metabolites_QTL_1 and not metabolites_QTL_2:
            metabolites1,QTL1 = metabolites_QTL_1
            metabolites2,QTL2 = ['N/A','N/A']
        elif not metabolites_QTL_1 and metabolites_QTL_2:
            metabolites2,QTL2 = metabolites_QTL_2
            metabolites1,QTL1 = ['N/A','N/A']
        else:
            metabolites1,QTL1 = ['N/A','N/A']
            metabolites2,QTL2 = ['N/A','N/A']
        metabolites = metabolites1 + '|' +metabolites2
        if QTL1 is None:
            QTL1 = 'N/A'
        if QTL2 is None:
            QTL2 = 'N/A'
        QTL = QTL1 +'|'+ QTL2
        #f_marker = (r_name,bin,metabolites,QTL)
        f_marker = (bin_,metabolites,QTL)
    else:            
        metabolites_QTL = conn.met_qtl(bin_)
        if metabolites_QTL:
            metabolites,QTL = metabolites_QTL
            #f_marker = (r_name,bin,metabolites,QTL)
            f_marker = (bin_,metabolites,QTL)
        else:
            #f_marker = (r_name,bin)
            f_marker = (bin_,'N/A','N/A')
    conn.close()
    return f_marker  
    
def precublast(r_name,mirna,r_ini,numero,dbname=DB_NAME):
    # OJO: MIRAR ESTA CONEXION, SACARLA?
    '''
    Document this
    '''
    conn = DBInterac(dbname)
    if numero!=0:
        c = conn.datafrom_precu_blast_ali(r_name,mirna,r_ini)
    else:
        c = conn.datafrom_precu_blast_micro(r_name,mirna,r_ini)
    conn.close()
    return c

def readmiranda(mirna):
    conn = DBInterac(DB_NAME)
    out = conn.r_miranda(mirna)
    conn.close()
    return out

def chunker(xx,s=70):
    for i in range(0,len(xx),s):
        yield xx[i:i+s]

@post('/microResult')
@get('/microResult/<micro_number>')
@view('microresult')
def microResult(micro_number=''):
    # buscar q_name en miranda

    if not micro_number:
        mirna = request.forms.get('micro_val','DEFAULT')
        metab = request.forms.get('metab','').replace('|','')
        fromto = request.forms.get('fromto','').replace('|','')        
        C_hitDef = request.forms.get('hitdef','').replace('|','')
        C_alig = request.forms.get('alig','').replace('|','')
        C_exp = request.forms.get('exp','').replace('|','')
        C_xls = request.forms.get('xls','').replace('|','')
    else:
        mirna = micro_number.replace('|','').replace(';','')
        metab = fromto = C_hitDef = C_alig = C_exp = C_xls = 'on'
    
    tpl_d = {'page_type': 'microResult', 'mirna':mirna, 
             'page_title' : 'Search by micro, results',
             'metab':metab, 'C_hitDef':C_hitDef, 'C_alig':C_alig,
             'C_exp':C_exp, 'fromto':fromto, 'C_xls':C_xls}
    tpl_d['miranda_ss'] = readmiranda(mirna)
    tpl_d['expression_s'] = EXPRESSION_S
    conn = DBInterac(DB_NAME)
    seq_ori = conn.seq_from_mirnas(mirna)
    seq_br = '<br>'.join(chunker(seq_ori))
    tpl_d['seq'] = seq_br 
    tpl_d['pubs'] = _carga_pubs(mirna)
    # verifico si mirna esta en alignname de precu_blast para ver que 
    # busqueda hago.
    numero = conn.count_align(mirna)
    tpl_d['numero'] = numero
    queryname = {}
    markers2 = {}    
    for miranda_row in tpl_d['miranda_ss']:
        r_name = miranda_row[2]
        r_ini = miranda_row[5]
        #mirna
        parID = miranda_row[0]
        tmp = precublast(r_name,mirna,r_ini,numero,DB_NAME)
        # desenrrolar tmp, poner fn d alineamiento y volver a enrollar.
        new_tmp = []
        for sub_tmp in tmp:
            sub_tmp = list(sub_tmp)
            sub_tmp[4] = _align_var(sub_tmp[4],sub_tmp[6], sub_tmp[7],80)
            new_tmp.append(sub_tmp)
            # para recorrer uno solo, Ariel lo pidio asi.
            break
        if new_tmp:
            queryname[parID] = new_tmp
        # busqueda bin
        tmp = conn.bin_from_parid(parID)
        if tmp:
            bin_ = tmp[0]
            markers2[r_name] = metayqtl(bin_)
    tpl_d['queryname'] = queryname
    tpl_d['markers2'] = markers2
    tpl_d['STATIC_URL'] = STATIC_URL
    tpl_d['type'] = 'microresult'

    conn.close()
    return tpl_d

@post('/targetResult')
@get('/targetResult/<target>')
@view('targetresult')
def targetResult(target=''):
    if not target:
        fromto = request.forms.get("fromto","").replace('|','')
        target = request.forms.get('target_val','DEFAULT').replace('|','')
        metab = request.forms.get("metab","").replace('|','')
        C_hitDef = request.forms.get('hitdef','').replace('|','')
        C_alig = request.forms.get('alig','').replace('|','')
        C_exp = request.forms.get('exp','').replace('|','')
        C_xls = request.forms.get('xls','').replace('|','')
    else:
        target = target.replace('|','').replace(';','')
        #try:
        #    dot = req.environ['selector.vars']['dot']
        #    target += '.'+dot
        #except KeyError:
        #    pass
        fromto = metab = C_hitDef = C_alig = C_exp = C_xls = 'on'
    tpl_d = {'page_type': 'targetResult', 'target':target, 
             'page_title' : 'Search by target, results',
             'metab':metab, 'C_hitDef':C_hitDef, 'C_alig':C_alig,
             'C_exp':C_exp, 'fromto':fromto, 'C_xls':C_xls}
    #tpl_d['miranda_ss'] = readmiranda(mirna)
    tpl_d['expression_s'] = EXPRESSION_S
    conn = DBInterac(DB_NAME)
    #seq_ori = conn.seq_from_mirnas(mirna)
    tpl_d['miranda_ss'] = conn.miranda_rname(target)
    queryname = {}
    parID = conn.parID_from_target(target)
    if parID:
        bin_ = conn.bin_from_parid(parID[0])
        markers2 = metayqtl(bin_[0]) if bin_ else ''
    else:
        markers2 = ''
    tpl_d['markers2'] = markers2
    
    for rec in tpl_d['miranda_ss']:
        mirna = rec[1]
        tpl_d['numero'] = conn.count_align(mirna)
        r_name = rec[2]
        r_ini = rec[5]
        parID = rec[0]
        tmp = precublast(r_name,mirna,r_ini,tpl_d['numero'])
        # desenrrolar tmp, poner fn d alineamiento y volver a enrollar.
        new_tmp = []
        for sub_tmp in tmp:
            sub_tmp = list(sub_tmp)
            sub_tmp[4] = _align_var(sub_tmp[4],sub_tmp[6], sub_tmp[7],80)
            new_tmp.append(sub_tmp)
            # para recorrerlo solo una vez porque Ariel quiere
            # que se vea un solo resultado.
            break
        if new_tmp:
            queryname[parID] = new_tmp
    tpl_d['queryname'] = queryname
    # del target, tomar los markers!
    # verificar si es SGN o no.
    if 'SGN-' in target:
        # busco el BAC container
        tmp1 = conn.bac_unigenesbacs_target(target)
        if tmp1:
            # bacfromu es el bac q viene de unigene_bacs
            tpl_d['bac_from_u'] = tmp1[0]
            tmp = conn.markerid_bacmarkers_bacs(tmp1[0])
        else:
            # hacer algo si no hay bac
            tpl_d['bac_from_u'] = 'N/A'
            tmp = None
    else:
        tmp = conn.markerid_bacmarkers_bacs((target,))
    markers = set()
    if tmp:
        for markid in tmp:
            tmp_mark = conn.mcp_markers_markerid(markid)
            if tmp_mark:
                markers.add((markid[0],tmp_mark[0],tmp_mark[1],tmp_mark[2]))
    tpl_d['markers'] = markers
    tpl_d['STATIC_URL'] = STATIC_URL
    conn.close()
    return tpl_d

@post('/blastresult_ax')
@view('blastresult_ax')
def blastresult_ax():

    b_exe = settings.BLASTN_EXE
    d = {'seq':request.forms.get('SEQUENCE',''),
         'eval':request.forms.get('EXPECT','10'),
         'db':request.forms.get('DB','micro'),}
    #return ('<pre>'+str(d)+'</pre>')

    _ws = '' if d['db']=='target' else 7 
    b_db = os.path.join(settings.BLASTDB_PATH,'%s.fasta'%d['db'])
    if _ws:
        cli = str(blastcli(cmd=b_exe,db=b_db,evalue=d['eval'],word_size=_ws,outfmt=5)).split(' ')
    else:
        cli = str(blastcli(cmd=b_exe,db=b_db,evalue=d['eval'],outfmt=5)).split(' ')
    print cli
    with open(settings.ERROR_LOG, "w") as fherror:
         fherror.write(" ".join(cli)+"\n")
    p = subprocess.Popen(cli, env=os.environ, stdin=subprocess.PIPE, 
                         stdout=subprocess.PIPE)
    std = p.communicate(input=d['seq'])[0]
    lblast = []
    try:
        for rec in NCBIXML.parse(StringIO(std)):
            for align in rec.alignments:
                lblast.append((align.hit_def, align.hsps[0].expect, align.hsps[0].score))
    except:
        pass
        # TD: Error log
    d['lblast'] = lblast
    cl = (' '.join(cli)).replace(settings.BLASTDB_PATH,'')
    d['cl'] = cl
    
    return d    


@post('/binResult')
@get('/binResult/<bin_number>')
@view('binresult')
def binResult(bin_number=''):

    if bin_number:
        bin_ = bin_number
        qtl_s = meta_s = hitdef_s = fromto = metab = C_hitDef = C_alig = C_exp = C_xls = 'on'
    else:
        bin_ = request.forms.get('bin', '').replace('|','')
        fromto = request.forms.get("fromto","").replace('|','')
        metab = request.forms.get("metab","").replace('|','')
        C_hitDef = request.forms.get('hitdef','').replace('|','')
        C_alig = request.forms.get('alig','').replace('|','')
        C_exp = request.forms.get('exp','').replace('|','')
        C_xls = request.forms.get('xls','').replace('|','')

    tpl_d = {'page_type': 'binResult', 'bin':bin_, 
             'page_title' : 'Search by Bin, results',
             'metab':metab, 'C_hitDef':C_hitDef,
             'C_alig':C_alig, 'C_exp':C_exp,
             'fromto':fromto, 'C_xls':C_xls}
    tpl_d['expression_s'] = EXPRESSION_S
    conn = DBInterac(DB_NAME)
    tpl_d['miranda_ss'] = conn.bin1(bin_)
    queryname = {}
    for rec in tpl_d['miranda_ss']:
        mirna = rec[1]
        numero = conn.count_align(mirna)
        tpl_d['numero'] = numero
        r_name = rec[2]
        r_ini = rec[5]
        parID = rec[0]
        tmp = precublast(r_name,mirna,r_ini,numero)
        new_tmp = []
        for sub_tmp in tmp:
            sub_tmp = list(sub_tmp)
            sub_tmp[4] = _align_var(sub_tmp[4],sub_tmp[6], sub_tmp[7],80)
            new_tmp.append(sub_tmp)
            # para recorrerlo solo una vez porque Ariel quiere
            # que se vea un solo resultado.
            break
        if new_tmp:
            queryname[parID] = new_tmp
    tpl_d['queryname'] = queryname
    tpl_d['markers2'] = metayqtl(bin_)
    tpl_d['STATIC_URL'] = STATIC_URL
    tpl_d['type'] = 'searchbin'
    conn.close()
    return tpl_d
        

@post('/keywordResult')
@view('keywordresult')
def keywordResult():
    keywords = request.forms.get('searchkey', '').replace('|','')
    qtl_s = request.forms.get('qtl_s', '').replace('|','')
    meta_s = request.forms.get('meta_s', '').replace('|','')
    hitdef_s = request.forms.get('hitdef_s', '').replace('|','')
    fromto = request.forms.get("fromto","").replace('|','')
    metab = request.forms.get("metab","").replace('|','')
    C_hitDef = request.forms.get('hitdef','').replace('|','')
    C_alig = request.forms.get('alig','').replace('|','')
    C_exp = request.forms.get('exp','').replace('|','')
    
    tpl_d = {'page_type': 'keywordResult', 'keywords':keywords, 
             'page_title' : 'Search by Keywords, results',
             'fromto':fromto,'metab':metab,'C_hitDef':C_hitDef,
             'C_alig':C_alig, 'C_exp':C_exp}
             
    tpl_d['expression_s'] = EXPRESSION_S
    conn = DBInterac(DB_NAME)
    allbins = set()
    # checo q campos hay que buscar:
    if qtl_s:
        #busco en qtl
        bins1 = conn.bin_from_bins_qtl(keywords)
        if bins1:
            allbins |= set([x[0] for x in bins1])
    if meta_s:
        # busco en metabolites de la tabla bins
        bins2 = conn.bin_from_bins_metab(keywords)
        if bins2:
            allbins |= set([x[0] for x in bins2])
    # con todos estos bines, buscar todos los parID!
    # tabla tmp
    conn_tt = TempTables(DB_NAME)
    c = conn_tt.get_parIDs(allbins)
    allparid_set = set([x[0] for x in c])
    tpl_d['miranda_ss'] = conn_tt.all_miranda_parID()
    if hitdef_s:
        hitdef_res = conn_tt.par_ID_from_keys(keywords)
        if hitdef_res:
            allparid_set2 = set([x[0] for x in hitdef_res])
            parid_diff = allparid_set2.difference(allparid_set)
            # ahora si busco los datos
            tpl_d['miranda_ss'].extend(conn_tt.create_kk3(parid_diff))
    tpl_d['qtls'] = qtl_s
    conn_tt.close()
    conn.close()
    queryname = {}
    markers2 = {}
    for rec in tpl_d['miranda_ss']:
        mirna = rec[1]
        conn = DBInterac(DB_NAME)
        numero = conn.count_align(mirna)
        tpl_d['numero'] = numero    
        r_name = rec[2]
        r_ini = rec[5]
        parID = rec[0]
        conn.close()
        tmp = precublast(r_name,mirna,r_ini,numero)
        new_tmp = []
        for sub_tmp in tmp:
            sub_tmp = list(sub_tmp)
            sub_tmp[4] = align_var(sub_tmp[4],sub_tmp[6], sub_tmp[7],80)
            new_tmp.append(sub_tmp)
            # para recorrerlo solo una vez porque Ariel quiere
            # que se vea un solo resultado.
            break
        if new_tmp:
            queryname[parID] = new_tmp
        conn = DBInterac(DB_NAME)
        tmp = conn.bin_from_parid(parID)
        conn.close()
        if tmp:
            bin_ = tmp[0]
            markers2[r_name] = metayqtl(bin_)
    tpl_d['queryname'] = queryname
    tpl_d['markers2'] = markers2
    tpl_d['STATIC_URL'] = STATIC_URL
    conn.close()
    return tpl_d
    
if not is_server:
    run(host='localhost', port=8080)
else:
    import bottle
    application = bottle.default_app()


