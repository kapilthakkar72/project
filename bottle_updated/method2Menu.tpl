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
	<b><a href="/method1">Method 1</a></b> | <b><a href="/method2">Method 2</a></b> | <b><a href="/method3">Method 3</a></b>

	<br><br>
	
	<h2>Method 2:</h2>

	<form action="/diffPlot" method="post">
		
		<table id="input">
		<tr>
			<td align="right">See result:<br> </td>
			<td><input type="radio" name="opt" value="statewise" required>Statewise
			<input type="radio" name="opt" value="centerwise" required>Centerwise</td>
		</tr>
		<tr>
			<td align="right">Use Smoothed Data:<br> </td>
			<td><input type="radio" name="smoothedData" value="Yes" required>Yes
			<input type="radio" name="smoothedData" value="No" required>No (Original Data will be used)</td>
		</tr>
		<tr class="alt">
			<td align="right">Select Centers:</td>
			<td><select name="center" style="width: 150px" > 
			%for s in centers:
				<option value={{ s }} name={{ s }}>{{ s }}</option>
			%end 
			</select></td>
		</tr>
		<tr>
			<td align="right">Select State:</td>
			<td><select name="state" style="width: 150px" >
			%for s in states:
				<option value="{{ s }}" name="{{ s }}">{{ s }}</option>
			%end 
				<option value="0" name="0">All States</option>
			</select><i> (if all states chosen than modal price will be taken as average for each state)</i></td>
		</tr>
		<tr class="alt">
			<td align="right">Variation <i>(Retail Price Diff : Today - Given days before)</i>:</td><td> <input type="text" name = "variation" value =7 style="width: 150px" ><i> (Note that it may not be exact 7 days before. If some data is missing than it will cosider the price which was available )</i></td>
		</tr>
		
		<tr>
			
			<td align="right"><b>Time input : Option 1 </b><br><br>
							  Select Year:  <br> <br>
							  Select Month:
			</td>
			<td> <br><br>
				<select name="year" style="width: 150px" > 
			%for y in years:
				<option value={{ y }} name={{ y }}>{{ y }}</option>
			%end 
				<option value="0" name="0">All Years</option>
			</select>
			
			<br><br>
			
			<select name="month" style="width: 150px" >
				<option value="0" name="0">All Months</option>
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
			</td>
		</tr>
		
		<tr>
			
			<td align="right"><b>Time input : Option 2 </b><br><br>
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
				
		<tr>
			<td align="right">Time Input :<br> </td>
			<td><input type="radio" name="timeInput" value="option1" required>Option 1
			<input type="radio" name="timeInput" value="option2" required>Option 2</td>
		</tr>
		
		<tr>
			<td align="right">Data To Plot:</td>
			<td>
				<input type="checkbox" name="wholesalePriceC" value="wholesalePriceC" checked>Wholesale Price<br>
				<input type="checkbox" name="retailPriceC" value="retailPriceC" checked>Retail Price <br>
				<input type="checkbox" name="absoluteDiffC" value="absoluteDiffC" checked>Absolute Difference <br>
				<input type="checkbox" name="relativeDiffC" value="relativeDiffC" checked>Relative Differnce (wrt wholesale) <br>
				<input type="checkbox" name="arrivalC" value="arrivalC" checked>Arrival <br>
				<input type="checkbox" name="retailDiff" value="retailDiff" checked>Difference in Retail Prices <br>
				<input type="checkbox" name="rmwAnalysis" value="rmwAnalysis" checked>Wholesale minus Retail Analysis<br>
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