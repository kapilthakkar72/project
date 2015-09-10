<html>
	<head>
		<style> 
			#input {
			    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
			    border: 1px solid #98bf21;
			}

			#input td, #input th {
			    font-size: 1em;
			    border: 1px solid #98bf21;
			    padding: 3px 7px 2px 7px;
			}

			#input th {
			    font-size: 1.1em;
			    text-align: left;
			    padding-top: 5px;
			    padding-bottom: 4px;
			    background-color: #A7C942;
			    color: #ffffff;
			}

			#input tr.alt td {
			    color: #000000;
			    background-color: #EAF2D3;
			}
		</style>
	</head>
<body>
	<h1> Analysis of Onion Data </h1>
	<b><b><a href="/method2">Method 2</a></b> 

	<br><br>
	
	<h2>Method 2:</h2>

	<form action="/diffPlot" method="post">
		
		<table id="input">
		
		
		<tr class="alt">
			<td align="right">Select Centers:</td>
			<td><select name="center" style="width: 150px" > 
			%for s in centers:
				<option value={{ s }} name={{ s }}>{{ s }}</option>
			%end 
			</select></td>
		</tr>		
		
		<tr class="alt">
			
			<td align="right"><b>Time input</b><br><br>
								 Select Start Month: <br> <br>
								 Select Start Year:  <br> <br>
								 Select End Month: <br> <br>
								 Select End Year:  <br> <br>
								 
			</td>
			<td>
				
				<br><br>			
				<select name="start_month" style="width: 150px" >
					<option value="1" name="1">January</option>
					<option value="2" name="2">February</option>
					<option value="3" name="3">March</option>
					<option value="4" name="4">April</option>
					<option value="5" name="5">May</option>
					<option value="6" name="6">June</option>
					<option value="7" name="7">July</option>
					<option value="8" name="8">August</option>
					<option value="9" name="9">September</option>
					<option value="10" name="10">October</option>
					<option value="11" name="11">November</option>
					<option value="12" name="12">December</option>
				</select>
				
				<br> <br>
				
				<select name="start_year" style="width: 150px" > 
				%for y in years:
					<option value={{ y }} name={{ y }}>{{ y }}</option>
				%end 
				</select>
				
				<br> <br>
				
				<select name="end_month" style="width: 150px" >
					<option value="1" name="1">January</option>
					<option value="2" name="2">February</option>
					<option value="3" name="3">March</option>
					<option value="4" name="4">April</option>
					<option value="5" name="5">May</option>
					<option value="6" name="6">June</option>
					<option value="7" name="7">July</option>
					<option value="8" name="8">August</option>
					<option value="9" name="9">September</option>
					<option value="10" name="10">October</option>
					<option value="11" name="11">November</option>
					<option value="12" name="12">December</option>
				</select>
				
				<br> <br>
				
				<select name="end_year" style="width: 150px" > 
					%for y in years:
						<option value={{ y }} name={{ y }}>{{ y }}</option>
					%end 
				</select>
				
				<br><br>			
			</td>
		</tr>
		<tr class="alt">
			<td align="right">Data To Plot:</td>
			<td>
				<input type="checkbox" name="wholesalePriceC" value="wholesalePriceC" checked>Wholesale Price<br>
				<input type="checkbox" name="retailPriceC" value="retailPriceC" checked>Retail Price <br>
				<input type="checkbox" name="arrivalC" value="arrivalC" checked>Arrival <br>
			</td>
		</tr>
		
		<tr class="alt">
			<td colspan=2 style="padding-left:260px"><input type="Submit" value="Submit" name="Submit"/></td>
		</tr>
		</table>
	</br>
	</form>
</body>
</html>