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
	
	<h2>Method 3:</h2>

	<form action="/plotHisto" method="post">
		
		<table id="input">
		
		<tr class="alt">
			<td align="right">Select Centers:</td>
			<td><select name="center" style="width: 150px" > 


			%for i in range(0,len(centers)):
				<option value={{ centreids[i] }} name={{ centers[i] }}>{{ centers[i] }}</option>
			%end 
			</select></td>
		</tr>
		
		
		<tr>
			<td align="right">Select Year:</td>
			<td><select name="year" style="width: 150px" > 
			%for y in years:
				<option value={{ y }} name={{ y }}>{{ y }}</option>
			%end 
				<option value="0" name="0">All Years</option>
			</select></td>
		</tr>
		<tr class="alt">
			<td align="right">Select Month:</td>
			<td><select name="month" style="width: 150px" >
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
			<i>(if all months chosen than modal price will be taken as average for whole year)</i></td>
		</tr>
		<tr class="alt">
			<td colspan=2 style="padding-left:260px"><input type="Submit" value="Submit" name="Submit"/></td>
		</tr>
		</table>
	</br>
	</form>
</body>
</html>