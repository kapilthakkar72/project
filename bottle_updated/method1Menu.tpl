<html>
<body>
	<h1> Analysis of Onion Data </h1>
	<b><a href="/method1">Method 1</a></b> | <b><a href="/method2">Method 2</a></b> | <b><a href="/method3">Method 3</a></b>

	<br><br>


	<form action="/cluster" method="post">

		Select State:
		<select name="state">
		%for s in states:
			<option value={{ s }} name={{ s }}>{{ s }}</option>
		%end
			<option value="0" name="0">All States</option>
		</select> (if all states chosen than modal price will be taken as average for each state)

		<br><br>

		Select Year:
		<select name="year">
		%for y in years:
			<option value={{ y }} name={{ y }}>{{ y }}</option>
		%end
		</select>

		<br><br>

		Select Month:
		<select name="month">
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
		(if all months chosen than modal price will be taken as average for whole year)
		<br><br>

		<input type="Submit" value="Submit" name="Submit"/>

	</br>
	</form>
</body>
</html>