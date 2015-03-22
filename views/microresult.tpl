
#include "views/common_header.tpl"

<div class="well">


<h1>Results for micro: <result>$mirna</result></h1>

<h2>Publications</h2>

#for $pub in $pubs
$pub[0][0][:-1] , $pub[0][1] , $pub[0][2]<br/>
${', '.join($pub[1])}
<br>

<br>
#end for

<h2>Precursor Sequence</h2>
<p class="dnaseq">$seq</p>
<br>
<p>
</p>

#if len($miranda_ss)>=2:
<h2>Predicted targets</h2>
#else
<h2>Predicted target</h2>
#end if
<p></p>

#for $m in $miranda_ss:

<table class="table table-bordered">
<tr><th class="info">Target name</th><td><a href="/targetResult/$m[2]">$m[2]</a></td></tr>
<tr><th class="info">Micro position</th><td>$m[3] to $m[4]</td></tr>
#if $fromto:
<tr><th class="info">Target position</th><td>$m[5] to $m[6]</td></tr>
#end if

#if $C_alig:
<tr><th class="info">Alignment</th><td><img src="/static/imgs/aligns/align-${m[0]}.png" width=500 height=80 alt="alignment" /></td></tr>
#end if

#if $C_hitDef:
<tr><th colspan="2" class="warning">Gene annotation</th></tr>
<tr><th class="info">Augustus gene prediction</th>
<td>
#if $m[12]==1:
Yes
#else
No
#end if
</td></tr>
<tr><th class="info">Genome threather vs SGN unigenes supporting alignment</th>
<td>
#if $m[14]:
$m[14]
#else
N/A
#end if
</td>
</tr>
<tr><th class="info">Arabidopsis peptide alignment (Blast x)</th>
<td>
#if $m[13]:
$m[13]
#else
N/A
#end if
</td>
</tr>
#if $m[2].startswith('SGN-'):
<tr><th class="info">SGN Unigene annotation</th>
<td>
#if $m[15]:
$m[15]
#else
No significant hits detected for this target or not run.
#end if
</td></tr>
#else
<tr><th class="info">MicroRNA precursor alignment</th><td>
#if $m[0] in $queryname
#for $q in $queryname[$m[0]]
<p>
#* m0 y q: $m[0] $q *#
Putative function precursor 
#if $numero == 0
$q[5]
#else
$mirna
#end if
<br />
parid: $q[0]<br />
e: $q[1]<br />
ident: $q[2]%<br />
bit: $q[3]<br />
seq: $q[4]<br />
</p>
#end for
#else
N/A
#end if
</td></tr>
#end if

#end if
#if $C_exp:
#set $expname = $m[2] + '.png'
#if $expname in $expression_s:
<tr><th class="info">Expression</th><td><img src="/static/imgs/exp/${expname}" alt="expression data" /></td></tr>
#end if
#end if
#if $metab:
<tr><th colspan="2" class="warning">Target genetic Map Location</th></tr>
<tr><th class="info">Bin name</th><td>

#if $m[2] not in $markers2
N/A</td></tr>
<tr><th class="info">Metabolite (QML)</th><td>N/A</td></tr>
<tr><th class="info">QTL</th><td>N/A</td></tr>
#else
<a href="/binResult/$markers2[$m[2]][0]">$markers2[$m[2]][0]</a></td></tr>
<tr><th class="info">Metabolite (QML)</th><td>$markers2[$m[2]][1]</td></tr>
<tr><th class="info">QTL</th><td>$markers2[$m[2]][2]</td></tr>
#end if

#end if

</table>
<p>
<hr>
</p>
#end for

#if $C_xls:
Excel dump: <a href="/static/xls/tmpmicro/${mirna}.xls">$mirna</a>
#end if






</div>	

#include "views/common_footer.tpl"