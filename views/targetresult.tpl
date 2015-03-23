
#include "views/common_header.tpl"

<div class="well">






<p>
<h1>Results for target: <result>$target</result></h1>
</p>

#* Si es SGN, poner el bac container *#
#if $target.startswith('SGN-'):
<h2>BAC holding Unigene: $bac_from_u</h2>
#end if

<h2>Markers</h2>

<table class='table table-striped'>
<tr class="info"><th>Name</th><th>Map</th><th>Chromosome</th><th>Position</th></tr>
<tbody>
#if $markers:
#for $m in $markers:
<tr><td>$m[0]</td><td>$m[1]</td><td>$m[2]</td><td>$m[3]</td></tr>
#end for
#else
<tr><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td></tr>
#end if
</tbody>
</table>


<hr/>


#if $metab:
<h2>Target Genetic Map Location</h2>
<table class='table'>
<tr class='info'><th>Bin name</th><th>Metabolite (QML)</th><th>QTL</th></tr>
#if not $markers2
<tr><td>N/A</td><td>N/A</td><td>N/A</td></tr>
#else
<tr><td>$markers2[0]</td><td>$markers2[1]</td><td>$markers2[2]</td></tr>
#end if
</table>
<hr/>
#end if


#if $C_exp:
<h2>Expression</h2>
#set $expname = $target + '.png'
#if $expname in $expression_s:
<img src="/static/imgs/exp/${expname}" alt="expression data" />
#else
N/A
#end if
<hr/>
#end if

#if len($miranda_ss)>=2:
<h2>Predicted targets</h2>
#else
<h2>Predicted target</h2>
#end if
<p></p>


#for $m in $miranda_ss:
<table class="table table-bordered">
<tr><th class="info">miRNA</th><td><a href="/microResult/$m[1]">$m[1]</a></td></tr>
<tr><th class="info">Micro position</th><td>$m[3] to $m[4]</td></tr>
#if $fromto:
<tr><th class="info">Target position</th><td>$m[5] to $m[6]</td></tr>
#end if
#if $C_alig:
<tr><th class="info">Alignment</th><td><img src="/static/imgs/aligns/align-${m[0]}.png" width=500 height=80 alt="alignment" /></td></tr>
#end if
#if $C_hitDef
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
</td></tr>
<tr><th class="info">Arabidopsis peptide alignment (Blast x)</th>
<td>
#if $m[13]:
$m[13]
#else
N/A
#end if
</td></tr>
#if $target.startswith('SGN-'):
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
#* $mirna *#
$m[1]
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


#* esto comentout xq en target tendria q estar once
#if $C_exp:
#set $expname = $m[2] + '.png'
#if $expname in $expression_s:
<tr><td>Expression</td>
	<td><img src="/static/exp/${expname}" alt="expression data"></td>
</tr>
#end if
#end if
*#


</table>
<p>
<hr>
</p>


#end for


#if $C_xls:
Excel dump: <a href="/static/xls/tmptarget/${target}.xls">$target</a>
#end if


</div>
#include "views/common_footer.tpl"
