#------------------------------------------------------------------------
# app/CommandProcessor.py
#------------------------------------------------------------------------
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CommandProcessor:
    def __init__(self, app):
        self.app = app

    def processFile(self, commandFile):
        if Path(commandFile).exists():
            logger.info(f'Process commands from file {commandFile}')
            with open(commandFile, 'r') as fin:
                icmd = 0
                for line in fin.readlines():
                    if len(line) == 0 or line[0] == '#': continue
                    line = line.strip()
                    if len(line) == 0: continue
                    self.processString(line)
                    icmd += 1
            logger.info(f'  processed {icmd} commands from file {commandFile}')
        pass
    
    def processString(self, commandString):
        logger.debug(f'  process command "{commandString}"')
        words = commandString.split()
        if len(words) == 0:
            return None
        commandName = words[0]
        args = [ word.split(',')
                 if word.find(',')>=0 else word
                 for word in words[1:] ]
        return self.processCommand(commandName, *args)
        
    def processCommand(self, cmdName, *args):
        match cmdName:
            case 'addImage': self.app.addImage(*args)
            case 'addImagesFromJson': self.app.readImagesFromJson(*args)
            case 'selectImages':
                if len(args)==1:
                    arg = [args[0]] if type(args[0])==str else args[0]
                    self.app.selectImages(arg)
                else:
                    logger.warning('selectImages need argument <imageName> or <imageName1>,<imageName2>,...')
            case 'selectAnalysis': self.app.selectAnalysis(*args)
            case 'setAnalysisName': self.app.setAnalysisName(*args)
            case 'setAnalysisParameter':
                self.app.setAnalysisParameter(*args)
            case 'runAnalysis': self.app.runAnalysis()
        return True
    
    
