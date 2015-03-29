#include "views/common_header.tpl"

<div class="well">

<h1>Select a search:</h1>
<br />



<div class="btn-group" data-toggle="buttons">
  <label class="btn btn-primary" id="btnbin" onmouseout="hideTooltip()" onmouseover="showTooltip(event,'Delimited chromosome fraction on the genetic map of the S. pennellii introgression lines population');return false">
    <input type="radio" name="options" id="option1bin" autocomplete="off"> Bin
  </label>
  <label class="btn btn-primary" id="mirnacb" onmouseout="hideTooltip()" onmouseover="showTooltip(event,'Name of the plant microRNA');return false">
    <input type="radio" name="options" id="option2mirna" autocomplete="off"> miRNA
  </label>
  <label class="btn btn-primary" id="targetcb" onmouseout="hideTooltip()" onmouseover="showTooltip(event,'Putative target name; could be a Bacterial Artificial Chromosome (BAC) anchored to the tomato genome or an Unigene (<a href=\'http://www.sgn.cornell.edu\'>SGN</a>)');return false">
    <input type="radio" name="options" id="option3target" autocomplete="off"> Target
  </label>
  <label class="btn btn-primary" id="keywordcb" onmouseout="hideTooltip()" onmouseover="showTooltip(event,'Search by keyword in fields: QTL and/or Metabolites and/or Hit Definition.');return false">
    <input type="radio" name="options" id="option4keyword" autocomplete="off"> Keyword
  </label>
</div>



<div ID="searchbin">
<h2>Search by Bin</h2> 
<p class="bg-info">Select a bin from the drop-down menu.</p> 
<form action="binResult" method="post" class="form-inline"> 
<div class="form-group">

<label for="binsel">Bin
<select id="binsel" name="bin" class="form-control">
#include "views/binlist.tpl"
</select></label>

</div>
#include "views/displayopts.tpl"

<div ID="searchmicro">
<h2>Search by Micro</h2> 
<p class="bg-info">Select a micro from the drop-down menu.</p> 
<form action="microResult" method="post" class="form-inline"> 
<div class="form-group">
<label for="microsel"> Micro code 
	<select id="microsel" name="micro_val" class="form-control">
#include "views/microlist.tpl"
</select></label>
</div>
#include "views/displayopts.tpl"

<div ID="searchtarget">
<h2>Search by Target</h2> 
<p class="bg-info">Enter a target name like "SGN-U566117", "C02SLe0022J22.1" (without  quotes).</p> 
<form action="targetResult" method="post">

<label for="myInput">Target name:</label> 
<div id="myAutoComplete">
	<input name="target_val" id="myInput" type="text"> 
	<div id="myContainer"></div> 
</div> 
<script type="text/javascript" src="/${STATIC_URL}/js/data3.js"></script> 

 <br />
#include "views/displayopts.tpl"

<div ID="searchkey">
<h2>Search by Keyword</h2> 
<p class="bg-info">Enter a keyword like "copper", "resistance" (without  quotes).</p> 
  <form action="keywordResult" method="post"> 
  <label for="skey">Keyword to search :</label> <input name="searchkey" type="text" value="" size=30 id="skey" /> 
<br/>
<label for="qtl">Fields to search:</label>
  <div id="qtl">
  <input name="qtl_s" type="checkbox" checked > 
    QTL <input name="meta_s" type="checkbox" checked > Metabolites <input name="hitdef_s" type="checkbox" checked /> 
    Hit Definition</div> 
<br> 
#include "views/displayoptsnoxml.tpl"

</div>
#include "views/common_footer.tpl"

