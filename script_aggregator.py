#!/usr/bin/env python

#
# Copyright 2012 Red Hat Inc., Durham, North Carolina.
# All Rights Reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Authors:
#      "Martin Preisler" <mpreisle@redhat.com>
#

from xml.etree import ElementTree
from datetime import date
import os.path
import ConfigParser
    
sce_system_name = "http://open-scap.org/XMLSchema/SCE-definitions-1"

last_given_rule_id_suffix = 0
def generate_rule_id(prefix = "rule-"):
    global last_given_rule_id_suffix
    
    last_given_rule_id_suffix += 1
    
    return "%s%i" % (prefix, last_given_rule_id_suffix)

def rule_to_element(filepath, dscpath):
    title_text = filepath
    description_text = "STUB"

    if dscpath is not None:
        try:
            config = ConfigParser.RawConfigParser()
            config.read(dscpath)
            
            title_text = config.get("HEADER", "NAME")
            description_text = config.get("HEADER", "DESCRIPTION")
            
        except Exception as e:
            print("Parsing config file '%s' failed (exception: %s)" % (dscfile, e))
    
    ret = ElementTree.Element("Rule")
    ret.set("id", generate_rule_id())
    ret.set("selected", "true")
    
    title = ElementTree.Element("title")
    title.text = os.path.basename(title_text)
    ret.append(title)
    
    description = ElementTree.Element("description")
    description.text = os.path.basename(description_text)
    ret.append(description)
    
    check = ElementTree.Element("check")
    check.set("system", sce_system_name)
    ret.append(check)
    
    check_content_ref = ElementTree.Element("check-content-ref")
    check_content_ref.set("href", filepath)
    check.append(check_content_ref)
    
    return ret

import argparse

parser = argparse.ArgumentParser(description = "Aggregates given scripts and generates XCCDF that references them all")
parser.add_argument("--dscprefix", type = str, nargs = "?", help = "Prefix to a folder with .dsc files")
parser.add_argument("--output", type = str, default = "output.xccdf", help = "Path of the output file")
parser.add_argument("globs", metavar = "F", type = str, nargs = "+",
                   help = "File or glob of the check script(s)")

args = parser.parse_args()

import glob
files = []
for g in args.globs:
    gfiles = glob.glob(g)
    files.extend(gfiles)
    if len(gfiles) == 0:
        print("No file matches '%s'" % (g))

root = ElementTree.Element("Benchmark")
root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
root.set("xmlns", "http://checklists.nist.gov/xccdf/1.1")
root.set("id", "STUB")

status = ElementTree.Element("status")
status.set("date", date.today().strftime("%Y-%m-%d"))
status.text = "draft"
root.append(status)

title = ElementTree.Element("title")
title.text = "STUB"
root.append(title)

description = ElementTree.Element("description")
description.text = "STUB"
root.append(description)

notice = ElementTree.Element("notice")
notice.set("id", "disclaimer")
notice.text = "This XCCDF has been automatically generated, it should only serve as a baseline!"
root.append(notice)

front_matter = ElementTree.Element("front-matter")
front_matter.text = "STUB"
root.append(front_matter)

rear_matter = ElementTree.Element("rear-matter")
rear_matter.text = "STUB"
root.append(rear_matter)

reference = ElementTree.Element("reference")
reference.set("href", "STUB")
root.append(reference)

platform = ElementTree.Element("platform")
platform.set("idref", "cpe:/o:redhat:enterprise_linux:6")
root.append(platform)

version = ElementTree.Element("version")
version.text = "0.1"
root.append(version)
  
for file in files:
    file_basename = os.path.basename(file)
    
    dsc_basename = file_basename[0:file_basename.rfind(".")] + ".dsc"
    dscpath = os.path.join(args.dscprefix, dsc_basename)
    if not os.path.exists(dscpath):
        if args.dscprefix:
            print("Can't find dsc for '%s'. Looked for it at '%s'." % (file, dscpath))
            
        dscpath = None
        
    element = rule_to_element(file, dscpath)
    root.append(element)

# taken from http://effbot.org/zone/element-lib.htm#prettyprint
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

indent(root)
with open(args.output, "w") as f:
    f.write(ElementTree.tostring(root, "utf-8"))
    