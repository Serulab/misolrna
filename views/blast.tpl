#include "views/common_header.tpl"

<div class="well">

<div id="MainBlastForm">
<form name="MainBlastForm" id="blastform">
Enter sequence below in FASTA format 
<BR> 
<textarea name="SEQUENCE" rows=6 cols=60 id="example">&#062;Sequence Name
cagtgcagtcagctatgcgagtcagtcatcgaactcacgactcacggcatgcat
cgagcaacagcttagcattagccgaatgtcggctacgccgtacgtagtctatag</textarea>

<p></p>

Expect
<select name="EXPECT" id="expect"> 
    <option>0.0001</option>
    <option>0.001</option>
    <option>0.01</option>
    <option>1</option>
    <option selected>10</option> 
    <option>100</option>
    <option>1000</option>
</select> 

Database
<select name="DB" id="db"> 
    <option selected value = "micro">Micros</option> 
    <option value = "target">Targets</option> 
    <option value = "precus">Precursors</option> 
</select> 

<INPUT TYPE="submit" VALUE="Search" id="submitir"> 
</FORM> 
</div>

<div id="ajaxblastres"></div>





</div>
#include "views/common_footer.tpl"

