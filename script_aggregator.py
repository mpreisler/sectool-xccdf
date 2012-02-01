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

sce_system_name = "http://open-scap.org/XMLSchema/SCE-definitions-1"

last_given_rule_id_suffix = 0
def generate_rule_id(prefix = "rule-"):
    global last_given_rule_id_suffix
    
    last_given_rule_id_suffix += 1
    
    return "%s%i" % (prefix, last_given_rule_id_suffix)

def rule_to_element(filepath):
    ret = ElementTree.Element("Rule")
    ret.set("id", generate_rule_id())
    ret.set("selected", "true")
    
    title = ElementTree.Element("title")
    title.text = "STUB"
    ret.append(title)
    
    check = ElementTree.Element("check")
    check.set("system", sce_system_name)
    ret.append(check)
    
    check_content_ref = ElementTree.Element("check-content-ref")
    check_content_ref.set("href", filepath)
    check.append(check_content_ref)
    
    return ret

import argparse

parser = argparse.ArgumentParser(description = "Aggregates given scripts and generates XCCDF that references them all")
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
    element = rule_to_element(file)
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
print(ElementTree.tostring(root, "utf-8"))
