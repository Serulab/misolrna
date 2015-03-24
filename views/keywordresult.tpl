
#include "views/common_header.tpl"
<div class="well">

<h1>Results for keyword: <result>$keywords<result></h1>

#if len($miranda_ss)>=2:
<h2>Predicted targets</h2>
#else
<h2>Predicted target</h2>
#end if
<p></p>

#for $m in $miranda_ss:
#set $target = $m[2]
<table class='table table-bordered'>
<tr><th class='info'>Target name</th><td><a href="/targetResult/$m[2]">$m[2]</a></td></tr>
<tr><th class='info'>Micro name</th><td><a href="/microResult/$m[1]">$m[1]</a></td></tr>
<tr><th class='info'>Micro position</th><td>$m[3] to $m[4]</td></tr>
#if $fromto:
<tr><th class='info'>Target position</th><td>$m[5] to $m[6]</td></tr>
#end if
<tr><th colspan="2" class='warning'>Gene annotation</th></tr>
<tr><th>Augustus gene prediction</th>
<td>
#if $m[12]==1:
Yes
#else
No
#end if
</td></tr>
<tr><th class='info'>Genome threather vs SGN unigenes supporting alignment</th>
#if $m[14]:
#set $destacado = $m[14].replace($keywords,'<b class="dest">'+$keywords+'</b>')
<td>$destacado</td></tr>
#else:
<td>N/A</td></tr>
#end if
<tr><th class='info'>Arabidopsis peptide alignment (BlastX)</th>
#if $m[13]:
#set $tipo = str(type($m[13]))
##set $destacado = 'xx'
#set $destacado = $m[13].replace($keywords,'<b class="dest">'+$keywords+'</b>')

<td>$destacado</td></tr>
#else:
<td>N/A</td></tr>
#end if

#if $target.startswith('SGN-'):
<tr><th class='info'>SGN Unigene annotation</th>
<td>
#if $m[15]:
## cambiar esto por REGEX y hacerlo en SGN Unigene annotation.
## re.sub(regex, replacement, subject)
#set $destacado = $m[15].replace($keywords,'<b class="dest">'+$keywords+'</b>').replace($keywords.upper(),'<b class="dest">'+$keywords+'</b>').replace($keywords.capitalize(),'<b class="dest">'+$keywords.capitalize()+'</b>')
$destacado
#else
No significant hits detected for this target or not run.
#end if
</td></tr>
#else
<tr><th class='info'>MicroRNA precursor alignment</th><td>
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
E value: $q[1]<br />
Ident: $q[2]%<br />
Bit: $q[3]<br />
Alignment (query/subject): $q[4]<br />
</p>
#end for
#else
N/A
#end if
</td></tr>
#end if
#if $C_alig:
<tr><th class='info'>Alignment</th><td><img src="/static/imgs/aligns/align-${m[0]}.png" width=500 height=80 alt="alignment" /></td></tr>
#end if
#set $expname = $m[2] + '.png'
#if $expname in $expression_s:
<tr><td>Expression</td><td><img src="/static/imgs/exp/${expname}" alt="expression data" /></td></tr>
#end if

#if $metab:
<tr><th colspan="2" class='warning'>Target genetic Map Location</th></tr>
<tr><th>bin name</th><td>

#if $m[2] not in $markers2
N/A</td></tr>
<tr><th class='info'>Metabolite (QML)</th><td>N/A</td></tr>
<tr><th>QTL</th><td>N/A</td></tr>
#else
<a href="/binResult/$markers2[$m[2]][0]">$markers2[$m[2]][0]</a></td></tr>
<tr><th class='info'>Metabolite (QML)</th>
<td>
#if $markers2[$m[2]][1]:
#set $destacado = $markers2[$m[2]][1].replace($keywords,'<b class="dest">'+$keywords+'</b>').replace($keywords.upper(),'<b class="dest">'+$keywords+'</b>').replace($keywords.capitalize(),'<b class="dest">'+$keywords.capitalize()+'</b>')
$destacado
#else
N/A
#end if
</td>
</tr>
<tr><th class='info'>QTL</th><td>
#if $markers2[$m[2]][2]:
#set $destacado = $markers2[$m[2]][2].replace($keywords,'<b class="dest">'+$keywords+'</b>').replace($keywords.upper(),'<b class="dest">'+$keywords+'</b>').replace($keywords.capitalize(),'<b class="dest">'+$keywords.capitalize()+'</b>')
$destacado
#else
N/A
#end if
</td></tr>
#end if

#end if


</table>
<p>
<hr>
</p>
#end for



</div>
#include "views/common_footer.tpl"
