import relate_funs
class class_analysis_mo_ra:
    def __init__(self, patientID,planname,statelist,path2analog,save2name):
        self.patientID=patientID
        self.planname=planname
        self.statelist=statelist
        self.savename=save2name
        self.path2analog=path2analog
        if path2analog==None and patientID!=None and planname!=None:
            self.path2analog='/u/ysheng/MyAIXd/projects/patients/'+self.patientID+'/4DdoseRecon/exec/'+self.planname+'/'+self.planname+'_motion_range_ana.log'
        elif path2analog!=None:
            self.path2analog = path2analog
            print(self.path2analog)
        else:
            print('error input, check if you have input the path to TRiPlog or patient ID and plan name')
        if self.savename==None:
            self.savename=''

        self.path2_motion_savefile = './motion_ana_logs/'
        self.path2_range_savefile = './range_ana_logs/'
        self.path2_motion_log = self.path2_motion_savefile+'00_mo_ra_ana_processing.log'
        self.path2_range_log = self.path2_range_savefile+'00_mo_ra_ana_processing.log'

        # self.path2_motion_savefile = '/home/yurii/Sheng/patient_data/'
        # self.path2_range_savefile = '/home/yurii/Sheng/patient_data/'
        # self.path2_motion_log='/home/yurii/Sheng/patient_data/'+'00_mo_ra_ana_processing.log'
        # self.path2_range_log='/home/yurii/Sheng/patient_data/'+'00_mo_ra_ana_processing.log'
        self.voilist = []
        self.writelinesinfo=[]

    def fun_analysis_motion(self,motionlist):  # dose_shown_in_gd is the dose written in the exec file, for SPHIC momi cases this value was set to 3 for all plans.
        print('-m actived. start motion analysis, dat file written in ./motion_ana_logs/00_motion_ana.dat')
        writedata='start write data for motion states: '
        for a in self.statelist:
            writedata += a+' '
        writedata += '\n'

        relate_funs.writelog(self.path2_motion_log, 'Start a new motion analysis')
        writeloginfo = 'running patient: ' + self.patientID + ' plan: ' + self.planname
        relate_funs.writelog(self.path2_motion_log, writeloginfo)
        # write analysis data


        for oarname in motionlist:
            writedata += self.patientID + ' ' + self.planname + ' ' + oarname
            for statename in self.statelist:
                #writedata+=' state'+statename+' '
                motiondata = self.fun_motion_info(oarname, statename)
                if motiondata=='9999':
                    errorinfo='either motion states or oarname wrongly defined. Please check.'
                    relate_funs.writelog(self.path2_motion_log, errorinfo)
                writedata += motiondata
            writedata += '\n'
        # save info and analysis data
        save_motion_filename=self.path2_motion_savefile+self.patientID+'_'+self.planname+'_'+self.savename+'_motion.txt'
        with open(save_motion_filename, 'w+') as savefileinfo:
            # savefileinfo.writelines('patientID plan VOI volume pre_dose parameter 3D 4D1 4D2 4D3 ...')
            savefileinfo.writelines(writedata)

    def fun_motion_info(self,oarname,motionstate):
        average_motion='9999'
        with open (self.path2analog,'r') as mo_ran_log_to_ana:
            for data_to_ana in mo_ran_log_to_ana:
                data_to_ana_list=data_to_ana.split()
                determin_state='ref to state '+motionstate
                if determin_state in data_to_ana:
                    if oarname in data_to_ana_list:
                        average_motion=data_to_ana[data_to_ana.rfind(':')+1:-3]
        return average_motion

    def fun_analysis_range(self,rangefield):
        print('-r actived. start range analysis, dat file written in ./range_ana_logs/02_range_ana.dat')
        writedata='start write data for motion states: 0 '
        for a in self.statelist:
            writedata += a+' '
        writedata += '\n'

        relate_funs.writelog(self.path2_range_log, 'Start a new range analysis')
        # write log
        writeloginfo = 'running patient: ' + self.patientID + ' plan: ' + self.planname
        relate_funs.writelog(self.path2_range_log, writeloginfo)
        # write analysis data
        writedata += self.patientID + ' ' + self.planname+' '
        for fieldname in rangefield:
            average_range0, standerror_range0 = self.fun_range_info(fieldname, '0')
            writedata += average_range0 + standerror_range0
            for statename in self.statelist:
                #writedata += ' F' + fieldname + 'MS'+statename+' '
                average_range,standerror_range = self.fun_range_info(fieldname, statename)
                if average_range == '9999' or standerror_range == '9999':
                    errorinfo = 'either motion states or Field name wrongly defined. Please check.'
                    relate_funs.writelog(self.path2_range_log, errorinfo)
                writedata += average_range+standerror_range
        writedata += '\n'
        # save info and analysis data
        save_range_filename = self.path2_range_savefile + self.patientID + '_' + self.planname + '_' + self.savename + '_range.txt'
        with open(save_range_filename, 'w+') as savefileinfo:
            # savefileinfo.writelines('patientID plan VOI volume pre_dose parameter 3D 4D1 4D2 4D3 ...')
            savefileinfo.writelines(writedata)

    def fun_range_info(self,fieldname, statename):
        average_range='9999'
        standerror_range='9999'
        startline=0
        endline=0
        with open (self.path2analog,'r') as mo_ran_log_to_ana:
            datalineall=mo_ran_log_to_ana.readlines()
            dataline=0
            for data_to_ana in datalineall:
                dataline+=1
                if 'getH2Orange' in data_to_ana:
                    data_to_ana_list=data_to_ana.split()
                    if fieldname in data_to_ana_list:
                        startline=dataline
                if startline!=0 and '<TIME>' in data_to_ana:
                    endline=dataline
                    break
            dataline = 0
            for data_to_ana in datalineall:
                dataline += 1
                if dataline>startline and dataline<endline:
                    dertermin_state='Ranges for state '+statename
                    if dertermin_state in data_to_ana:
                        startline=dataline
                        endline=dataline+12
                        break
            dataline = 0
            for data_to_ana in datalineall:
                dataline += 1
                if dataline >= startline and dataline <= endline:
                    if 'mean' in data_to_ana:
                        average_range=data_to_ana[data_to_ana.rfind(':')+1:-3]
                    if 'std deviation' in data_to_ana:
                        standerror_range=data_to_ana[data_to_ana.rfind(':')+1:-3]
                        break
        return average_range,standerror_range