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
								 Select Start Date: <br> <br>
								 Select End Date:  <br> <br>
						
								 
			</td>
			<td>
				
				<br><br>
				<input type="date" name="start_date">
				<br> <br>
				<input type="date" name="end_date">
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