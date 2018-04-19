import os
import re
import time
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from helloworld import app

from flask import request, render_template, flash, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '.\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getTS():
    return time.time()
app.jinja_env.globals.update(getTS=getTS)

@app.route('/upload/', methods=['GET', 'POST'])
def fileupload():
    filename = None
    if request.method == 'POST':
        if 'uploaded' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
        #filelist = request.files.getlist('uploaded')
        #print(filelist)
        file = request.files['uploaded']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            ## Validating filename
            accepted_ext = ['.evtx', '.csv']
            file_name, file_ext = os.path.splitext(filename)
            if file_ext not in accepted_ext:
                flash('File Type is not supported. Please upload \
                        csv,xls,or xlsx.')
                #return render_template('fileupload.html')
                return redirect(request.url)

            fileurl = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fileurl)
            print('File Location:', fileurl)
            ## Process Data
            if file_ext == '.evtx':
                fileurl = process_evtx(fileurl)
                filename = os.path.basename(fileurl)
            df = eventlog_readdata(fileurl)
            eventsourcecolor_df = eventsource_color(df)
            toperrors, dictlist_id = toptenerror(df)
            toperrors = toperrors.index.tolist()
            main_detailseq_df, main_seq_df = eventsequencing(df)
            sankeyvalue, sankeycolor = eventsankey(main_seq_df, eventsourcecolor_df)
            print(sankeyvalue)
            #return redirect(url_for('uploaded_file', filename=filename))
            return render_template('fileupload.html',
                                   filename=filename,
                                   toperrors=toperrors,
                                   dictlist_id=dictlist_id,
                                   sankeyvalue=sankeyvalue,
                                   sankeycolor=sankeycolor)
    return render_template('fileupload.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def process_evtx(fileurl):
    print('**** Process EVTX File ****')
    fileoutput = fileurl.replace('.evtx','.csv')
    fileinput = fileurl
    print(fileinput, '\n', fileoutput)
    cmdstring = "logparser " + \
                    "\"SELECT * INTO " + fileoutput + \
                    " FROM " + fileinput + "\" " + \
                    "-i:EVT -o:CSV"
    print(cmdstring)
    os.system(cmdstring)

    print('**** End Process EVTX File ****')
    return fileoutput

def validate_format_type():
    pass

def process_uploaded_file(fileurl=None):
    print('Process FILE')
    if fileurl:
        filename = os.path.basename(fileurl)
        df = pd.read_csv(fileurl, encoding='mbcs')
        
        #### Preparing and Cleaning Data ####
        ## Appending columns with more info
        df['LogType'] = re.search("(System|Application)", filename).group(0)
        df['Filename'] = filename

        ## Remove unneeded columns
        drops = ['EventLog', 'TimeWritten', 'SID', 'Data', 'Strings', 'Message']
        df = df.drop(drops, axis=1)
        del drops
        
        ## Parse Date and Time
        dfdatetime = df['TimeGenerated'].str.split(" ")
        df['Date'] = [item[0] for item in dfdatetime]
        df['Time'] = [item[1] for item in dfdatetime]
        del dfdatetime

        ## Order based on Date and Time
        df.sort_values(by=['Date', 'Time'], inplace=True)

        ## Add Hour Column
        hour = [t[0:2] for t in df['Time']]
        hour = [h + ":00:00" for h in hour]
        df['Hour'] = hour
        del hour

        ## Combine Event + SourceName
        eventid = df['EventID']
        sourcename = df['SourceName']
        df['EventSource'] = [str(e) + ' - ' + s for e, s in zip(eventid, sourcename)]
        del(eventid, sourcename)
        return df

def eventlog_readdata(fileurl):
    # Read the file
    print("**** Start EventLog_ReadData Script ****")
    df = pd.read_csv(fileurl, nrows=2, encoding='mbcs')

    # Check number of columns. 7 = hyperV | 15 = parsed.
    if df.shape[1] == 7:
        print("***HyperV Log***")
        # HyperV logic
        fields = ['EventID', 'LogType', 'ServerName', 'Description',
                  'SourceName', 'DateTime', 'EventTypeName']
        df = pd.read_csv(fileurl, header=0, names=fields, encoding='mbcs')

        # Parsing DateTime
        dfdatetime = df['DateTime'].str.split("T")
        df['Date'] = [item[0] for item in dfdatetime]
        df['Time'] = [item[1] for item in dfdatetime]
        del dfdatetime

        # FileType
        df['FileName'] = os.path.basename(fileurl)

        df = df[['DateTime', 'Date', 'Time', 'EventID', 'LogType', 'SourceName', 'EventTypeName',
                 'ServerName', 'Description', 'FileName']]

        #print(df.head())

    elif df.shape[1] == 15:
        print("***Parsed Log***")
        # ParsedLog logic
        fieldsToRead = ['EventLog', 'EventID', 'EventTypeName', 'SourceName',
                        'ComputerName', 'TimeWritten', 'Message']
        df = pd.read_csv(fileurl, usecols=fieldsToRead, encoding='mbcs')
        # adding filename column
        df['FileName'] = os.path.basename(fileurl)

        # adding logtype
        #logtype = os.path.splitext(os.path.basename(fileloc))[0]
        logtype = df["EventLog"].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
        df['LogType'] = logtype.str.extract('(System|Application)')
        del logtype

        # cleaning event type column
        df.EventTypeName = df.EventTypeName.str.replace(' event', '')

        # Parsing DateTime
        dfdatetime = df['TimeWritten'].str.split(" ")
        df['Date'] = [item[0] for item in dfdatetime]
        df['Time'] = [item[1] for item in dfdatetime]
        del dfdatetime

        # Renaming dataframe columns
        df.rename(columns={'ComputerName':'ServerName',
                           'TimeWritten':'DateTime',
                           'Message':'Description'}, inplace=True)
        print(df.info())

        df = df[['DateTime', 'Date', 'Time', 'EventID', 'LogType', 'SourceName', 'EventTypeName',
                'ServerName', 'Description', 'FileName']]

        #print(df.head())
    else:
        print("***Not HyperV or ParsedLog***")
    
    df.sort_values(by=['Date', 'Time'], inplace=True)

    ## Add Hour Column
    hour = [t[0:2] for t in df['Time']]
    hour = [h + ":00:00" for h in hour]
    df['Hour'] = hour

    ## Combine Event + SourceName
    eventid = df['EventID']
    sourcename = df['SourceName']
    df['EventSource'] = [str(e) + ' - ' + s for e, s in zip(eventid, sourcename)]
    del(eventid, sourcename)

    df = df[['DateTime', 'Date', 'Time', 'Hour', 'LogType', 'EventSource',
             'EventID', 'SourceName', 'EventTypeName', 'ServerName',
             'Description', 'FileName']]

    # Check output
    print(df.head())

    print("**** End EventLog_ReadData Script ****")
    return df

def eventsource_color(df):
    ## Define event type name list and color
    eventtypelist = ['Information', 'Warning', 'Error',
                     'Success', 'Failure', 'Critical', 'No Event']
    # information - blue, warning - yellow, error - salmon,
    # success - green, failure - red1, critical - red2
    eventcolorlist = ['#42A5F5', '#FFEB3B', '#EF5350',
                      '#43A047' , '#7B1FA2', '#B71C1C', '#99A3A4']
    eventcolor_df = pd.DataFrame({'EventTypeName':eventtypelist,
                                'EventColor':eventcolorlist})
    #print(eventcolor_df)

    ## Create a dataframe with only unique eventID - eventsource - eventtypename
    eventsource_df = df.copy().loc[:,['EventID', 'EventSource',
                                      'EventTypeName', 'LogType']].drop_duplicates()

    ## Specify 1 more event IDs for events prior to what has been recorded in event log
    # Insert value as list instead of singular value due to indexing error 
    # when passing as singular value
    extraevent_df = pd.DataFrame({'EventID' : [99999],
                                  'EventSource' : [None],
                                  'EventTypeName': ['No Event'],
                                  'LogType': [None]})
    eventsource_df = eventsource_df.append(extraevent_df)

    ## Add color to that dataframe
    eventsourcecolor = pd.merge(eventsource_df, eventcolor_df, on='EventTypeName')

    print(eventsourcecolor.head())
    
    return eventsourcecolor

def toptenerror(df):
    ## Top 10 Event ID error
    toperrors = df.ix[ df.EventTypeName.str.contains('Error', case=False) ]\
        .EventSource.value_counts()

    amchart_colorlist = ['#FF0F00', '#FF6600', '#FF9E01', '#FCD202', '#F8FF01',
    '#B0DE09', '#04D215', '#0D8ECF', '#0D52D1', '#2A0CD0']

    dictlist_id = []
    for i,row in enumerate(toperrors[:10].iteritems()):
        temp_dict = {'event':row[0], 'frequency':row[1], 
        'id':row[0].split(" - ")[0], 'color':amchart_colorlist[i]}
        dictlist_id.append(temp_dict)
    del(temp_dict, amchart_colorlist)
    print(dictlist_id)
    return toperrors[:10], dictlist_id

def eventsequencing(df):
    #### Creating Sequence of errors ####
    print("**** EVENT SEQUENCING ****")
    app_error = df.ix[ df.EventTypeName.str.contains('Error', case=False) & 
                     df.LogType.str.contains('Application|System', case=False) ]
    toperror = app_error.EventSource.value_counts()[:10]
    
    toperror = df.ix[ df.EventTypeName.str.contains('Error', case=False) & 
                     df.LogType.str.contains('Application|System', case=False) ].\
                     EventSource.value_counts().sort_index(kind='mergesort').\
                     sort_values(ascending=False)[0:9]
    
    ## Defining nth number of event sequence before and after main events
    prev_n = 10
    next_n = 0
    eventseq = list(range(-prev_n, next_n+1))

    ## Initialize dataframe
    main_detailseq_df = pd.DataFrame([])
    main_seq_df= pd.DataFrame([])

    for index, value in enumerate(toperror.index):

        ## Find index of certain error event
        #errorID = toperror.index[index]
        errorID = value
        indexloc = df.ix[df.EventSource == errorID].index.tolist()

        emptyList = []
        for i, val in enumerate(indexloc):
            seq_x = list(range(val-prev_n, val+next_n+1))
            emptyList.extend(seq_x)
        
        tempresultdf = df.ix[emptyList]
        tempresultdf['EventID'] = tempresultdf['EventID'].fillna(99999).astype(int)
        tempresultdf.loc[:, 'EventSequence'] = eventseq * len(indexloc)
        tempresultdf.loc[:, 'MainError'] = errorID
        tempresultdf.loc[:, 'NthOccurence'] = [item for item in range(1,len(indexloc)+1) for _ in range(len(eventseq))]

        ## Append result to main dataframe
        main_detailseq_df = main_detailseq_df.append(tempresultdf)
        
        ## Sequence Dataframe (in sequencing format)
        temp_seq_df = tempresultdf.pivot(index='NthOccurence', 
                                        columns='EventSequence', 
                                        values='EventID')
        temp_seq_df.loc[:,'EventSource'] = value
        errordatetime = tempresultdf.ix[tempresultdf.EventSequence==0].DateTime
        temp_seq_df.loc[:,'DateTime'] = errordatetime.values
        del errordatetime

        ## Append result to main dataframe
        main_seq_df = main_seq_df.append(temp_seq_df)
        #print(main_detailseq_df)

    return main_detailseq_df, main_seq_df

def eventsankey(main_seq_df, eventsourcecolor_df):
    print("\n**** SANKEY DATA PREP ****")
    ########## Sankey Data Preparation ##########
    
    # empty DF
    temp_df = pd.DataFrame([])
    tempcolor_df = pd.DataFrame([])

    sankey_df = main_seq_df.copy()
    
    # Drop irrelevant column
    
    sankey_df.drop(['EventSource','DateTime'], 1, inplace=True)

    # Drop rows with consecutive error IDs
    sankey_df = sankey_df.ix[sankey_df.loc[:,-1] != sankey_df.loc[:,0] ]

    # Loop
    for i in range(1, sankey_df.shape[1]):
        print('iteration', i)
        # build dataframe for sankey visualization
        col1 = sankey_df.columns[i-1]
        col2 = sankey_df.columns[i]

        grouped_df = sankey_df.groupby([col1, col2])
        freq = grouped_df.size().to_frame('n').reset_index()

        # rename 'from' and 'to' column
        freq.rename(columns = {col1:'from', col2:'to'}, inplace=True)

        # add column no to the row data
        freq['fromint'] = freq['from']
        freq['toint'] = freq['to']
        freq['from'] = freq['from'].astype(str) + '(' + str(i-1) + ')'
        freq['to'] = freq['to'].astype(str) + '(' + str(i) + ')'
        #print(freq)

        # append to original data
        temp_df = temp_df.append(freq)

    temp_df = temp_df[temp_df.n>2]
    # create list of unique node and color
    uniquenodelist = temp_df[['from', 'to']].copy().stack().\
                                                unique().tolist()
    uniquenodelist = [k.split('(')[0] for k in uniquenodelist]
    uniquenodelist = map(int, uniquenodelist)
    print(uniquenodelist)

    temp_df = temp_df[['from', 'to', 'n']]
    print(temp_df)
    print("\n**** END SANKEY DATA PREP ****")

    # colorlist
    colordict = dict(zip(eventsourcecolor_df['EventID'],
                         eventsourcecolor_df['EventColor']))

    #sankeycolorlist = ['#EF5350', '#42A5F5', '#42A5F5', '#EF5350']
    sankeycolorlist = [colordict[k] for k in uniquenodelist]
    print(sankeycolorlist)

    # return 'list' data since 'array' data doesnt have comma
    return temp_df.values.tolist(), sankeycolorlist
