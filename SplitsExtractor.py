#!/usr/bin/python3
import argparse
import datetime as dt
import xml.etree.ElementTree as ET
from enum import Enum


class XMLEnum(Enum):
    GameIcon = 0
    GameName = 1
    CategoryName = 2
    Metadata = 3
    Offset = 4
    AttemptCount = 5
    AttemptHistory = 6
    Segments = 7
    AutoSplitterSettings = 8


class SplitEnum(Enum):
    Name = 0
    Icon = 1
    SplitTimes = 2
    BestSegmentTime = 3
    SegmentHistory = 4


class TypeTime(Enum):
    RealTime = 0
    GameTime = 1


class Parse:
    def __init__(self, filepath, livesplit_enum):
        self.filepath = filepath
        self.enum = livesplit_enum

    # Get a game name and a category
    def getMainInfo(self):
        return '{} - {}'.format(self.getRoot()[XMLEnum.GameName.value].text,
                                self.getRoot()[XMLEnum.CategoryName.value].text)

    # Get root of xml
    def getRoot(self):
        self.handle = ET.parse(self.filepath)
        return self.handle.getroot()

    # Get array with splits and array size
    def getSplits(self):
        Splits = self.getRoot()[XMLEnum.Segments.value]
        SplitsNum = len(Splits)
        return Splits, SplitsNum

    # Get the history of the segments and return the last of them
    def getSegmentsHistory(self):

        HistoryBuffer = []
        History = self.getRoot()[XMLEnum.Segments.value]
        HistoryLen = len(History)

        for i in range(HistoryLen):
            TimerLen = len(History[i][SplitEnum.SegmentHistory.value])
            HistoryBuffer.append(History[i][SplitEnum.SegmentHistory.value][TimerLen - 1][TypeTime.GameTime.value].text)
        return HistoryBuffer

    # Convert text to time
    def text2time(self, text):
        return dt.datetime.strptime(text[:-4], "%H:%M:%S.%f")

    @staticmethod
    def time_sub(time1, time2):
        return time1 - time2

    @staticmethod
    def time_sum(time1, time2):
        return time1 + time2

    @staticmethod
    def init():

        if p:
            print(p.getMainInfo())
            try:
                Splits, SplitArraySize = p.getSplits()
                for i in range(SplitArraySize):
                    SplitName = Splits[i][SplitEnum.Name.value].text
                    BestIGTime = Splits[i][SplitEnum.BestSegmentTime.value][TypeTime.GameTime.value].text
                    PossibleSavePerSplit = p.time_sub(p.text2time(p.getSegmentsHistory()[i]),
                                                      p.text2time(BestIGTime))

                    if PossibleSavePerSplit.seconds >= 1:
                        print(
                                f'Name: {SplitName:>32}\tIGT: {p.text2time(p.getSegmentsHistory()[i]).time()} Best Segment: {p.text2time(BestIGTime).time()} | +{PossibleSavePerSplit}')
            except TypeError:
                pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", help="path to split file (*.lss)")
    args = parser.parse_args()

    if args.path:
        p = Parse(args.path, XMLEnum)
        if p:
            p.init()
    else:
        print("Usage: SplitsExtractor.py -h (--help)")
