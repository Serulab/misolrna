#!/usr/bin/env python

# LICENSE: AGPL 3.0. Sebastian Bassi

from selector import Selector
from yaro import Yaro
from tempfile import mkstemp
from bottle import SimpleTemplate
from bottle import route, run, view, static_file

import sys
sys.path.append("/var/www/misolrna.org/htdocs")
from dbconn import TempTables, DBInterac
from index_template import index_template as it
from cStringIO import StringIO
from Bio.Blast.Applications import NcbiblastnCommandline as blastcli
from Bio.Blast import NCBIXML

#from Cheetah.Template import Template

import os
import sys
import cPickle
import subprocess

BASE_URL = 'misolrna.org'
dbname = '/var/www/%s/htdocs/mirna20.db'%BASE_URL
rootdir = '/var/www/%s/htdocs/'%BASE_URL
imgdir = 'http://img.%s/'%BASE_URL
imgdirFS = '/var/www/%s/htdocs/img/'%BASE_URL
staticFS = '/var/www/%s/htdocs/img/static/'%BASE_URL

mirandaoutfile = '/root/misol/modificado/miRanda-1.9/src/mirandafull75plus'

#os.chdir(rootdir)

expression_s = set(['SGN-U577351.png', 'SGN-U317177.png', 'SGN-U577190.png', 'SGN-U581590.png', 'SGN-U564920.png', 'SGN-U314861.png', 'SGN-U564413.png', 'U217520.png', 'SGN-U580201.png', 'SGN-U219318.png', 'SGN-U575153.png', 'SGN-U225755.png', 'SGN-U573423.png', 'SGN-U315828.png', 'SGN-U573225.png', 'SGN-U579174.png', 'SGN-U580203.png', 'SGN-U576708.png', 'SGN-U579797.png', 'SGN-U313725.png', 'SGN-U313497.png', 'SGN-U574086.png', 'SGN-U312490.png', 'SGN-U567211.png', 'SGN-U315756.png', 'SGN-U319311.png'])

@route('/')
@view('index.tmp')
def index():
    #dataout = it(searchList=[{'page_type': 'home', 'page_title' : 'MiSolRNAdb Home page'}])
    return {}

@route('/static/css/<filename>')
def css_static(filename):
    return static_file(filename, root='/home/sbassi/projects/misolrna/static/css/')

@route('/static/fonts/<filename>')
def fonts_static(filename):
    return static_file(filename, root='/home/sbassi/projects/misolrna/static/fonts/')

@route('/static/js/<filename>')
def js_static(filename):
    return static_file(filename, root='/home/sbassi/projects/misolrna/static/js/')    

def search(req):
    dataout = it(searchList=[{'page_type': 'search', 'page_title' : 'Search miRNA'}])
    return str(dataout)
    
def help(req):
    dataout = it(searchList=[{'page_type': 'help', 'page_title' : 'Help page'}])
    return str(dataout)

def blast(req):
    dataout = it(searchList=[{'page_type': 'blast', 'page_title' : 'BLAST'}])
    return str(dataout)

def about(req):
    dataout = it(searchList=[{'page_type': 'about', 'page_title' : 'About Us'}])
    return str(dataout)


def rss(req):
    return open(rootdir+'rss.xml').read()    

def data3(req):
    return open(rootdir+'data3.js').read()
    
def toolt(req):
    return open(rootdir+'toolt.js').read()    
    
def part1(req):
    yield open(rootdir+'part1.fasta').read()    
    
def part2(req):
    yield open(rootdir+'part2.fasta').read()        
    
def part3(req):
    yield open(rootdir+'part3.fasta').read()        
    
def basiccss(req):
    return open(rootdir+'basic.css').read()

def tabscss(req):
    return open(rootdir+'tabs.css').read() 


def in4m(req):
    yield open(staticFS+'in4m.dmp').read()    
    
def t(req):
    yield open(rootdir+'t.txt').read()        
    
def status(req):
    yield """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head><title>Status</title></head>
<body>"""
    #yield "</body></html>"
    os.chdir('/var/www/misolrna.org/htdocs/')
    in4m = cPickle.load(open('in4m75plus.dmp'))
    ref = cPickle.load(open('ref.dmp'))
    I = len(in4m)
    R = len(ref)
    # get values in windows (tail).
    cmd = ['tail', mirandaoutfile]
    msize = os.path.getsize(mirandaoutfile)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    std = p.communicate()[0]
    for line in str(std).split('\n'):
        if line.startswith('>'):
            i = line.replace('>','').split('\t')[0]
            r = line.replace('>','').split('\t')[1]
            break
    iN = in4m.index(i)+1
    rN = ref.index(r)+1
    porc = ((float(((iN-1)*R)+rN))/(I*R))*100
    resto = 100-porc
    # checo status:
    cmd = ['ps', 'ax']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    std = p.communicate()[0]
    yield '<h2>Miranda Status</h2>\n'
    if 'miranda' in str(std):
        yield "RUNNING</br>"
    else:
        yield "STOPPED</br>"
    yield '<h2>Completion</h2>\n'
    yield '<img src="http://chart.apis.google.com/chart?chs=500x200&chd=t:%s,%s&cht=p3&chl=Done|Remaining"'%(porc,resto)
    
    yield "<br>Percent done: %.5f%% <br>"%porc
    yield "<br>Output file size: %s Mb</body></html>"%(msize/1000000.0)
    

def carga_pubs(mirna):
    ''' trae data de pubicaciones '''
    conn = DBInterac(dbname)
    pubsid = conn.pubids(mirna)
    publicaciones = []
    for pubid in pubsid:
        autoresid_l = [x[0] for x in conn.aid(pubid)]
        autores_l = []
        for autorid in autoresid_l:
            autores_l.append(conn.authorname(autorid))
        pubname = list(conn.articles(pubid))
        pubname[1] = conn.journals(pubname)
        #[x[0] for x in c3.fetchall()]
        publicaciones.append((pubname,autores_l))
    conn.close()
    return publicaciones
    
    
def align_var(s,u,v,ancho):
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
    conn = DBInterac(dbname)
    if '-' in bin_:
        # busco de a 1
        bin1 = bin_.split('-')[0]
        numero_bin = bin1[0] if len(bin1)==2 else bin1[:-1]
        #sacar parte numerica de bin1
        bin2_letra = bin_.split('-')[1]
        bin2 = numero_bin + bin2_letra
        #c3 = conn.cursor()
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
    
def precublast(r_name,mirna,r_ini,numero,dbname=dbname):
    # OJO: MIRAR ESTA CONEXION, SACARLA?
    conn = DBInterac(dbname)
    if numero!=0:
        c = conn.datafrom_precu_blast_ali(r_name,mirna,r_ini)
    else:
        c = conn.datafrom_precu_blast_micro(r_name,mirna,r_ini)
    conn.close()
    return c

def readmiranda(mirna):
    conn = DBInterac(dbname)
    out = conn.r_miranda(mirna)
    conn.close()
    return out

def chunker(xx,s=70):
   for i in range(0,len(xx),s):
       yield xx[i:i+s]


def microResult(req):
    # buscar q_name en miranda
    if req.environ['selector.vars'] == {}:
        mirna = req.form.get('micro_val','DEFAULT')
        metab = req.form.get("metab","").replace('|','')
        fromto = req.form.get("fromto","").replace('|','')        
        C_hitDef = req.form.get('hitdef','').replace('|','')
        C_alig = req.form.get('alig','').replace('|','')
        C_exp = req.form.get('exp','').replace('|','')
        C_xls = req.form.get('xls','').replace('|','')
    else:
        mirna = req.environ['selector.vars']['mirna'].replace('|','').replace(';','')
        metab = 'on'
        fromto = 'on'
        C_hitDef = 'on'
        C_alig = 'on'
        C_exp = 'on'
        C_xls = 'on'
    
    tpl_d = {'page_type': 'microResult', 'mirna':mirna, 
             'page_title' : 'Search by micro, results',
             'metab':metab, 'C_hitDef':C_hitDef, 'C_alig':C_alig,
             'C_exp':C_exp, 'fromto':fromto, 'C_xls':C_xls}
    tpl_d['miranda_ss'] = readmiranda(mirna)
    tpl_d['expression_s'] = expression_s
    conn = DBInterac(dbname)
    seq_ori = conn.seq_from_mirnas(mirna)
    seq_br = '<br>'.join(chunker(seq_ori))
    tpl_d['seq'] = seq_br 
    tpl_d['pubs'] = carga_pubs(mirna)
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
        tmp = precublast(r_name,mirna,r_ini,numero,dbname)
        # desenrrolar tmp, poner fn d alineamiento y volver a enrollar.
        new_tmp = []
        for sub_tmp in tmp:
            sub_tmp = list(sub_tmp)
            sub_tmp[4] = align_var(sub_tmp[4],sub_tmp[6], sub_tmp[7],80)
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
    dataout = it(searchList=[tpl_d])
    conn.close()
    return str(dataout)

def targetResult(req):
    if req.environ['selector.vars'] == {}:
        fromto = req.form.get("fromto","").replace('|','')
        target = req.form.get('target_val','DEFAULT').replace('|','')
        metab = req.form.get("metab","").replace('|','')
        C_hitDef = req.form.get('hitdef','').replace('|','')
        C_alig = req.form.get('alig','').replace('|','')
        C_exp = req.form.get('exp','').replace('|','')
        C_xls = req.form.get('xls','').replace('|','')
    else:
        target = req.environ['selector.vars']['name'].replace('|','').replace(';','')
        try:
            dot = req.environ['selector.vars']['dot']
            target += '.'+dot
        except KeyError:
            pass
        fromto = 'on'
        metab = 'on'
        C_hitDef = 'on'
        C_alig = 'on'
        C_exp = 'on'
        C_xls = 'on'
    tpl_d = {'page_type': 'targetResult', 'target':target, 
             'page_title' : 'Search by target, results',
             'metab':metab, 'C_hitDef':C_hitDef, 'C_alig':C_alig,
             'C_exp':C_exp, 'fromto':fromto, 'C_xls':C_xls}
    #tpl_d['miranda_ss'] = readmiranda(mirna)
    tpl_d['expression_s'] = expression_s
    conn = DBInterac(dbname)
    #seq_ori = conn.seq_from_mirnas(mirna)
    tpl_d['miranda_ss'] = conn.miranda_rname(target)
    queryname = {}
    parID = conn.parID_from_target(target)
    if parID:
        bin_ = conn.bin_from_parid(parID[0])
        if bin_:
            markers2 = metayqtl(bin_[0])
        else:
            markers2 = ''
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
            sub_tmp[4] = align_var(sub_tmp[4],sub_tmp[6], sub_tmp[7],80)
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
    dataout = it(searchList=[tpl_d])
    conn.close()
    return str(dataout)

# root@ubuntu:/var/www/sebastianbassi.com/htdocs# cp index_template.py /usr/lib/python2.5/site-packages/

def blastresult_ax(req):
    from Cheetah.Template import Template
    
    template_s = '''<h2>Blast result</h2><p></p>
#if $lblast:
<table border="1">
<tr><th>
#if $db=='micro':
Micro
#elif $db=='target':
Target
#elif $db=='precus':
Precursor
#end if
</th><th>E val</th><th>Score</th></tr>

#for $bdata in $lblast:
<tr><td>
#if $db=='micro':
<a href="/microResult/$bdata[0]">$bdata[0]</a></td><td>$bdata[1]</td><td>$bdata[2]
#elif $db=='target':
<a href="/targetResult/${bdata[0].split(' ')[0]}">${bdata[0].split(' ')[0]}</a></td><td>$bdata[1]</td><td>$bdata[2]
#elif $db=='precus':
<a href="/microResult/$bdata[0]">$bdata[0]</a></td><td>$bdata[1]</td><td>$bdata[2]
#end if
</td></tr>
#end for
</table>
#else
No results found
#end if

<p>Command line:</p> 
$cl <br/>

<p>Program used:</p>
BLAST 2.2.23 release (BMC Bioinformatics 2009, 10:421 doi:10.1186/1471-2105-10-421)<br/>'''
    
    b_exe = '/var/www/%s/htdocs/ncbi-blast-2.2.23+/bin/blastn'%BASE_URL    
    d = {'seq':req.form.get('SEQUENCE',''),
         'eval':req.form.get('EXPECT','10'),
         'db':req.form.get('DB','micro')}
    #return ('<pre>'+str(d)+'</pre>')
         
    _ws = ''
    if d['db']=='micro':
        b_db = '/var/www/%s/htdocs/micros.fasta'%BASE_URL
        _ws = 7
    elif d['db']=='target':
        b_db = '/var/www/%s/htdocs/target.fasta'%BASE_URL
    else:
        b_db = '/var/www/%s/htdocs/precus.fasta'%BASE_URL
        _ws = 7
    # hago el CLI
    if _ws:
        cli = str(blastcli(cmd=b_exe,db=b_db,evalue=d['eval'],word_size=_ws,outfmt=5)).split(' ')
    else:
        cli = str(blastcli(cmd=b_exe,db=b_db,evalue=d['eval'],outfmt=5)).split(' ')
    print cli
    open("/tmp/err.txt", "w").write(" ".join(cli)+"\n")
    p = subprocess.Popen(cli, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    std = p.communicate(input=d['seq'])[0]
    lblast = []
    try:
        for rec in NCBIXML.parse(StringIO(std)):
            for align in rec.alignments:
                lblast.append((align.hit_def, align.hsps[0].expect, align.hsps[0].score))
    except:
        pass
    d['lblast'] = lblast
    cl = (' '.join(cli)).replace('/var/www/%s/htdocs/'%BASE_URL,'')
    d['cl'] = cl
    dataout = Template(template_s, searchList=[d])
    return str(dataout)
    

def blastresult(req):
    b_exe = '/var/www/%s/htdocs/ncbi-blast-2.2.23+/bin/blastn'%BASE_URL

    
    d = {'page_title':'BLAST results',
         'page_type': 'blastresult', 
         'seq':req.form.get('SEQUENCE',''),
         'eval':req.form.get('EXPECT','10'),
         'db':req.form.get('DB','micro')}
         
    _ws = ''
    if d['db']=='micro':
        b_db = '/var/www/%s/htdocs/micros.fasta'%BASE_URL
        _ws = 7
    elif d['db']=='target':
        b_db = '/var/www/%s/htdocs/target.fasta'%BASE_URL
    else:
        b_db = '/var/www/%s/htdocs/precus.fasta'%BASE_URL
        _ws = 7
    # hago el CLI
    if _ws:
        cli = str(blastcli(cmd=b_exe,db=b_db,evalue=d['eval'],word_size=_ws,outfmt=5)).split(' ')
    else:
        cli = str(blastcli(cmd=b_exe,db=b_db,evalue=d['eval'],outfmt=5)).split(' ')
    p = subprocess.Popen(cli, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    std = p.communicate(input=d['seq'])[0]
    lblast = []
    for rec in NCBIXML.parse(StringIO(std)):
        for align in rec.alignments:
            lblast.append((align.hit_def, align.hsps[0].expect, align.hsps[0].score))
    
    d['lblast'] = lblast
    cl = (' '.join(cli)).replace('/var/www/%s/htdocs/'%BASE_URL,'')
    d['cl'] = cl
    dataout = it(searchList=[d])
    return str(dataout)

def binResult(req):
    if req.environ['selector.vars'] == {}:
        bin_ = req.form.get('bin', '').replace('|','')
        fromto = req.form.get("fromto","").replace('|','')
        metab = req.form.get("metab","").replace('|','')
        C_hitDef = req.form.get('hitdef','').replace('|','')
        C_alig = req.form.get('alig','').replace('|','')
        C_exp = req.form.get('exp','').replace('|','')
        C_xls = req.form.get('xls','').replace('|','')
    else:
        bin_ = req.environ['selector.vars']['bin'].replace('|','').replace(';','')
        fromto = 'on'
        metab = 'on'
        C_hitDef = 'on'
        C_alig = 'on'
        C_exp = 'on'
        C_xls = 'on'

    tpl_d = {'page_type': 'binResult', 'bin':bin_, 
             'page_title' : 'Search by Bin, results',
             'metab':metab, 'C_hitDef':C_hitDef,
             'C_alig':C_alig, 'C_exp':C_exp,
             'fromto':fromto, 'C_xls':C_xls}
    tpl_d['expression_s'] = expression_s
    conn = DBInterac(dbname)
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
            sub_tmp[4] = align_var(sub_tmp[4],sub_tmp[6], sub_tmp[7],80)
            new_tmp.append(sub_tmp)
            # para recorrerlo solo una vez porque Ariel quiere
            # que se vea un solo resultado.
            break
        if new_tmp:
            queryname[parID] = new_tmp
        #if tmp:
        #    queryname[parID] = tmp
        #markers2[r_name] = metayqtl(bin_)
    tpl_d['queryname'] = queryname
    tpl_d['markers2'] = metayqtl(bin_)
    dataout = it(searchList=[tpl_d])
    conn.close()
    return str(dataout)
        
def keywordResult(req):
    if req.environ['selector.vars'] == {}:
        keywords = req.form.get('searchkey', '').replace('|','')
        qtl_s = req.form.get('qtl_s', '').replace('|','')
        meta_s = req.form.get('meta_s', '').replace('|','')
        hitdef_s = req.form.get('hitdef_s', '').replace('|','')
        fromto = req.form.get("fromto","").replace('|','')
        metab = req.form.get("metab","").replace('|','')
        C_hitDef = req.form.get('hitdef','').replace('|','')
        C_alig = req.form.get('alig','').replace('|','')
        C_exp = req.form.get('exp','').replace('|','')
    else:
        keywords = 'low'
        qtl_s = 'on'
        meta_s = 'on'
        hitdef_s = 'on'
        fromto = 'on'
        metab = 'on'
        C_hitDef = 'on'
        C_alig = 'on'
        C_exp = 'on'
    
    tpl_d = {'page_type': 'keywordResult', 'keywords':keywords, 
             'page_title' : 'Search by Keywords, results',
             'fromto':fromto,'metab':metab,'C_hitDef':C_hitDef,
             'C_alig':C_alig, 'C_exp':C_exp}
             
    tpl_d['expression_s'] = expression_s
    conn = DBInterac(dbname)
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
    conn_tt = TempTables(dbname)
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
        conn = DBInterac(dbname)
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
        conn = DBInterac(dbname)
        tmp = conn.bin_from_parid(parID)
        conn.close()
        if tmp:
            bin_ = tmp[0]
            markers2[r_name] = metayqtl(bin_)
    tpl_d['queryname'] = queryname
    tpl_d['markers2'] = markers2
    
    dataout = it(searchList=[tpl_d])
    conn.close()
    return str(dataout)
    
    
s = Selector(wrap=Yaro)
#s.add('/', GET=index)
s.add('/status', GET=status)
s.add('/in4m.dmp', GET=in4m)
s.add('/t.txt', GET=t)

s.add('/part1.fasta', GET=part1)
s.add('/part2.fasta', GET=part2)
s.add('/part3.fasta', GET=part3)

s.add('/about', GET=about)
s.add('/keywordResult', POST=keywordResult)
s.add('/targetResult', POST=targetResult)
s.add('/targetResult/{name}.{dot}', GET=targetResult)
s.add('/targetResult/{name}', GET=targetResult)
s.add('/search', GET=search)
s.add('/help', GET=help)
s.add('/blast', GET=blast)
s.add('/blastresult', POST=blastresult)
s.add('/blastresult_ax', POST=blastresult_ax)
s.add('/binResult', POST=binResult)
s.add('/binResult/{bin}', GET=binResult)
s.add('/microResult', POST=microResult)
s.add('/microResult/{mirna}', GET=microResult)


application = s

run(host='localhost', port=8080)


