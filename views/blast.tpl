#include "views/common_header.tpl"

<div class="well">

<div id="MainBlastForm">
<form name="MainBlastForm" id="blastform" role="form">
<div class="form-group">    
    <label for="example">Enter sequence below in FASTA format</label> 
    <BR> 
    <textarea name="SEQUENCE" rows=6 cols=60 id="example">&#062;Sequence Name
cagtgcagtcagctatgcgagtcagtcatcgaactcacgactcacggcatgcat
cgagcaacagcttagcattagccgaatgtcggctacgccgtacgtagtctatag</textarea>
</div>
<p></p>

<label for="expect">Expect</label> 
<select name="EXPECT" id="expect"> 
    <option>0.0001</option>
    <option>0.001</option>
    <option>0.01</option>
    <option>1</option>
    <option selected>10</option> 
    <option>100</option>
    <option>1000</option>
</select> 

<label for="db">Database</label> 
<select name="DB" id="db"> 
    <option selected value = "micro">Micros</option> 
    <option value = "target">Targets</option> 
    <option value = "precus">Precursors</option> 
</select> 

<button type="submit" class="btn btn-default" id="submitir">Search</button>

</FORM> 
</div>

<div id="ajaxblastres"></div>





</div>
#include "views/common_footer.tpl"

