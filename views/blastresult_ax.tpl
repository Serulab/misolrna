<h2>Blast result</h2><p></p>
#if $lblast:
<table class="table">
<tr><th class="info">
#if $db=='micro':
Micro
#elif $db=='target':
Target
#elif $db=='precus':
Precursor
#end if
</th><th class="info">E val</th><th class="info">Score</th></tr>

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
BLAST 2.2.23 release (BMC Bioinformatics 2009, 10:421 <a href="http://www.biomedcentral.com/1471-2105/10/421">doi:10.1186/1471-2105-10-421</a>)<br/>