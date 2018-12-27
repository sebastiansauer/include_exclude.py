#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Quick-Typographie-Filter: include_exclude.py

  (C)opyleft in 2018 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  0.1   - 26.12.2018 (nm) - Erste Version
  0.2   - 27.12.2018 (nm) - "include-only" als Mischung von 
                            "exclude=all include=<taglist>" einbaut.

  WICHTIG:
  ========
    Benoetigt python3 !
    -> https://www.howtogeek.com/197947/how-to-install-python-on-windows/
    oder
    -> https://www.youtube.com/watch?v=dX2-V2BocqQ
    Bei *nix und macOS Systemen muss diese Datei als "executable" markiert
    sein!
    Also bitte ein
      > chmod a+x include_exclude.py
   ausfuehren!


  Lizenz:
  =======
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


import panflute as pf  # panflute fuer den pandoc AST
import logging  # logging fuer die 'include_exclude.log'-Datei

exclude_flag = False

"""
 Eine Log-Datei "include_exclude.log" erzeugen um einfacher zu debuggen
"""
DEBUGLEVEL = logging.ERROR  # .ERROR or .DEBUG  or .INFO
logging.basicConfig(filename='include_exclude.log', level=DEBUGLEVEL)


def prepare(doc):
    doc.tag_list = list(doc.get_metadata('tag', default=["all"]))
    logging.debug("Tags: "+str(doc.tag_list))


def intersection(lst1, lst2): 
    # Use of hybrid method for O(n) ...
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3 

def action(e, doc):
    """Main action function for panflute.
    """
    global exclude_flag
    
    logging.debug("-"*50)
    # logging.debug("current:" + str(e)+" next:"+str(e.next if getattr(e, "next", None) is not None else "---"))
    logging.debug("current:" + str(e))
    ret = e
    
    if isinstance(e, pf.Header):
        logging.debug("Header found: "+str(e.content))
        logging.debug("------------- Old exclude_flag: "+str(exclude_flag))
        exclude_flag = False
        include_list = []
        exclude_list = []
        
        if "include" in e.attributes:
            include_list = e.attributes["include"].split(",")
            
        if "exclude" in e.attributes:
            exclude_list = e.attributes["exclude"].split(",")
            
        uf "include-only" in e.attributes:
            exclude_list = ["all"]
            include_list =  e.attributes["include-only"].split(",")

        logging.debug("Tag-list    : "+str(doc.tag_list))
        logging.debug("Include-list: "+str(include_list))
        logging.debug("Exclude-list: "+str(exclude_list))

        if "all" in exclude_list:
            exclude_flag = True
            logging.debug("!------------ New exclude_flag: "+str(exclude_flag))
            ret = []
        
        if len(intersection(doc.tag_list, include_list)) > 0:
            exclude_flag = False
            ret = e

        if len(intersection(doc.tag_list, exclude_list)) > 0:
            exclude_flag = True
            logging.debug("!------------ New exclude_flag: "+str(exclude_flag))
            ret = []
            
        logging.debug("------------- New exclude_flag: "+str(exclude_flag))
        
    elif exclude_flag and not isinstance(e.next, pf.Header):
        logging.debug("next found: "+str(e))
        ret = []
    elif exclude_flag and isinstance(e.next, pf.Header):
        exclude_flag = False

    logging.debug("Next found: "+str(e))
    logging.debug("return:"+str(ret))
    return ret
            
def finalize(doc):
    pass


def main(doc=None):
    """main function.
    """

    logging.debug("Start style.py")
    ret = pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)
    logging.debug("End style.py")
    
    return ret


"""
 as always
"""
if __name__ == "__main__":
    main()
