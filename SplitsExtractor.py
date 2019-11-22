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
    def __init__(self, filepath, time, livesplit_enum):
        self.filepath = filepath
        self.enum = livesplit_enum
        self.time = time

    # Get a game name and a category
    def getMainInfo(self):
        return '{} - {}'.format(self.getRoot().find("GameName").text,
                                self.getRoot().find("CategoryName").text)

    # Get root of xml
    def getRoot(self):
        return ET.parse(self.filepath).getroot()

    # Get array with splits and array size
    def getSplits(self):
        Splits = self.getRoot().find("Segments")
        SplitsNum = len(Splits)
        return Splits, SplitsNum

    # Get the history of the segments and return the last of them
    def getSegmentsHistory(self):

        HistoryBuffer = []
        History, _ = self.getSplits()
        HistoryLen = len(History)

        for i in range(HistoryLen):
            #FIXME: the problem with the last element, why can't it be -1 ???
            HistoryBuffer.append(History[i].find("SegmentHistory")[-2][TypeTime.GameTime.value].text)
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
                for split_id in range(SplitArraySize):
                    SplitName = Splits[split_id].find("Name").text
                    BestIGTime = Splits[split_id].find("BestSegmentTime")[TypeTime.GameTime.value].text
                    PossibleSavePerSplit = p.time_sub(p.text2time(p.getSegmentsHistory()[split_id]),
                                                      p.text2time(BestIGTime))
                    if PossibleSavePerSplit.total_seconds() >= p.time:
                        print(f'Segment: {SplitName:>32}\tIGT: {str(p.text2time(p.getSegmentsHistory()[split_id]).time())[:-7]} Best Segment: {str(p.text2time(BestIGTime).time())[:-7]} | +{str(PossibleSavePerSplit)[:-7]}')
            except TypeError:
                pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", help="Path to split file (*.lss)")
    parser.add_argument("--time", "-t",
                        help="Number of seconds possible to save for each split. This option displays the splits, where you can save more time or equal to the specified one.",
                        type=int)
    args = parser.parse_args()

    if args.path and args.time:
        p = Parse(args.path, args.time, XMLEnum)
        if p:
            p.init()
    else:
        print("Usage: SplitsExtractor.py -h (--help)")