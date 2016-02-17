from bottle import get, post, request, run, response,template,redirect # or route

ResList=[]
CsvRelations=[]
CSVcount=0

@get('/home') # or @route('/login')
def home():
    return '''
        <form action="/home" method="post">
            Number Of CSVs: <input name="noOfCSVs" type="text" />
            <input value="Login" type="submit" />
        </form>
    '''

@post('/home') # or @route('/login', method='POST')
def do_home():
    noOfCSVs = request.forms.get('noOfCSVs')
    global CSVcount
    CSVcount=int(noOfCSVs)
    if noOfCSVs.isdigit():
        return template('CSVInputTemplate', csvCount=int(noOfCSVs))
    else:
        return "<p>Invalid Number.</p>"+str(noOfCSVs)

@get('/inputCSVs')
def inputCSVs():
    return "Finally"

@post('/inputCSVs')
def do_inputCSVs():
    global ResList
    for filename, file in request.files.iteritems():
    	Con = request.files[filename].name
	z=processFile(request.files.get(Con).file.readlines())
	ResList.append(z)
    te=""
    for i in request.forms.getall('CSVcheckBox'):
	te=te+ExponentialSmoothData(ResList[int(i)-1])
    return te
    redirect("/relationEntry")

@get('/relationEntry') # or @route('/login')
def relationEntry():
    return template('CSVRelationEntry', csvCount=CSVcount,resList= ResList)

@post('/relationEntry') # or @route('/login')
def do_relationEntry():
    global CsvRelations
    for i in range(CSVcount):
	temp=[]
	for j in range(CSVcount):
		val=request.forms.get(str(i+1)+"_"+str(j+1))
		temp.append(int(val))
	CsvRelations.append(temp)
    return printCSVAsList(CsvRelations)

def ExponentialSmoothData(csvList):
	dateofdata= [i[0] for i in csvList]
	array= [i[1] for i in csvList]
	s_date=dateofdata[0]
        end_date=dateofdata[-1]
	return smoothArray(s_date,dateofdata, array, end_date)

def smoothArray(s_date,dateofdata, array, end_date):
    array = np.array(array,dtype = float)
    start_date = s_date
    start_date = datetime.datetime.strptime(start_date, "%m/%d/%y").date()
    
    new_data = []
    prevVal = -1
    
    i=0 # To keep track over the arrays passed
    while(start_date <= end_date):
        if(start_date == dateofdata[i]):
            # data for this date is present
            if(i==0):
                # Simply add to final array
                prevVal = array[i]
                new_data.append([start_date,array[i]])                
            else:
                # Smooth
                if(prevVal == -1):
                    prevVal = array[i]
                    new_data.append([start_date,array[i]])
                else:
                    newVal = ( array[i] - prevVal ) * alpha + prevVal
                    new_data.append([start_date,newVal])
                    prevVal = newVal
            start_date = start_date + datetime.timedelta(days=1)
            i = i+1 
        else:
            # Data for this date is missing
            
            if(prevVal == -1):
                new_data.append([start_date,array[i]])
            else:
                new_data.append([start_date,prevVal])            
            start_date = start_date + datetime.timedelta(days=1)    
    return new_data

def printCSVAsList(csvList):
    te=""
    for x in csvList:
	for y in x:
		te=te+str(y)#str(y[0])+str(y[1])
    return te	

def processFile(csvFile):
	listOfData=[]
	for line in csvFile:
		listOfData.append((line.split(',')[0],line.split(',')[1]))
	return listOfData

run(host='localhost', port=8080, debug=True)
