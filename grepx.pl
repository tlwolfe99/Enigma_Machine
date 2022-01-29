#!/bin/perl -w
#=======================================================================
# My Grep Utility Written In Perl
#=======================================================================

use strict;
use DirHandle;
use fileHandle;


#-----------------------------------------------------------------------
# global variables
#
# CASESENSITIVE flag - case sensitive searches
# DEBUG         flag - display debug messages
# DIRCOUNT      count - directories processed
# FAILURE       return value - failure
# FILECOUNT     count - files processed
# MATCHCOUNT    count - number of matched found in processed files
# SUBDIR        flag - process subdirectories
# ROOTDIR       root directory
# STARTTIME     script start time
# SUCCESS       return value - success
# TOTALLINES    count - lines in all of the files processed
# VERBOSE       flag - display verbose messages
#-----------------------------------------------------------------------

my $CASESENSITIVE = 0;
my $DEBUG         = 0;
my $DIRCOUNT      = 0;
my $FAILURE       = 0;
my $FILECOUNT     = 0;
my $FILEPATTERN   = '\.php$';     # regular expression (escape any "/")
my $STRINGPATTERN = 'error';      # regular expression (escape any "/")
my $MATCHCOUNT    = 0;
my $SUBDIR        = 0;
my $ROOTDIR       = './';         # must end in "/"
my $STARTTIME     = time;
my $TOTALLINES    = 0;
my $SUCCESS       = 1;
my $VERBOSE       = 0;

# process command line arguments

if (ProcessCommandLineArguments() != $SUCCESS) { exit 1; }

# fix ROOTDIR
#   convert all '\' to '/'        (if any)
#   remove '/' from end-of-string (if any)
#   $ROOTDIR =~ s/\\/\//g;
#   if ($ROOTDIR =~ /^(.*)\/$/) { $ROOTDIR = $1; }


# display runtime environment

print "==================================================\n";
print 'Start time      = ' . localtime($STARTTIME) . "\n";
print "File pattern    = $FILEPATTERN\n";
print "Root dir        = $ROOTDIR\n";
print "Debug           = $DEBUG\n";
print "String pattern  = $STRINGPATTERN\n";
print "Subdir          = $SUBDIR\n";
print "Verbose         = $VERBOSE\n";
print "Case sensitive  = $CASESENSITIVE\n";
print "==================================================\n";

if (ProcessDirectoryTree($ROOTDIR,$FILEPATTERN,
                         $STRINGPATTERN) != $SUCCESS) { exit 1; }

 # display processing statistics

print "\n";
print "==================================================\n";
print "Dirs processed  = $DIRCOUNT\n";
print "Files processed = $FILECOUNT\n";
print "Matchs found    = $MATCHCOUNT\n";
print "Lines processed = $TOTALLINES\n";
print "==================================================\n";

exit 0;



#=======================================================================
#=======================================================================
#=======================================================================
# subroutines
#=======================================================================
#=======================================================================
#=======================================================================

#----------------------------------------------------------------------
# process a directory tree
#----------------------------------------------------------------------

sub ProcessDirectoryTree
{
   my $dir  = $_[0];              # directory (path and name)
   my $fpat = $_[1];              # file name match pattern
   my $spat = $_[2];              # string match pattern

   $DIRCOUNT++;                   # increment directory count

   if ($DEBUG) { print "\nProcessing Directory $dir\n"; }

   # get a list of all of the file names in the directory

   my $dh = new DirHandle;        # directory handle

   if (! opendir($dh,$dir))
   {
      print "\n";
      print "Error opening directory $dir\n";
      print "$!\n";
      print "\n";
      return $FAILURE;
    }

   my @fl = readdir $dh;          # array of file names

   closedir $dh;

   # process each file name

   my $f;                         # file name
   my $fs;                        # file specification (path + name)

   foreach $f (@fl)
   {
      # ignore  special cases

      if ($f eq ".")  { next; };
      if ($f eq "..") { next; };

      # create a file specification (path + name)

      $fs = $dir . $f;

      #  do not process subdirectories at this time

      if (-d $fs) { next; }

      # if it not a directory, does the file name match pattern
      # if yes, process the file

      if ($f =~ /$fpat/)
      {
	 if (ProcessFile($f,$fs,$spat) != $SUCCESS) { return $FAILURE; }
      }
   }

   if ($SUBDIR)                   # process subdirectories
   {
      foreach $f (@fl)
      {
         # ignore  special cases

         if ($f eq ".")  { next; };
         if ($f eq "..") { next; };

         # create a file specification (path + name)

         $fs = $dir . $f;

         #  process subdirectories

         if (-d $fs)
         {
            if (ProcessDirectoryTree($fs,$fpat,$spat) != $SUCCESS)
            { return $FAILURE; }
         }
      }
   }

   return $SUCCESS;
}


#-----------------------------------------------------------------------
# process a file
#-----------------------------------------------------------------------

sub ProcessFile

{
   my $f    = $_[0];           # file name
   my $fs   = $_[1];           # file specification (path + name)
   my $spat = $_[2];           # string pattern

   if ($DEBUG || $VERBOSE) { print "   Processing file $f\n"; }

   $FILECOUNT++;               # increment file count

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   # open the input and output files
   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

   if (! open(IN,"<$fs"))
   {
      print "\n";
      print "Error: can not open input file $fs\n";
      print "$!\n";
      print "\n";
      return $FAILURE;
   }

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   # read the file one line at a time
   # test if the string pattern matched the line
   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

   my $c  = 0;                 # file line number
   my $l;                      # line from file

   while(<IN>)
   {
      $l = $_;                 # copy the line

      chomp $l;                # remove trailing \n from the line 

      $c++;                    # increment line count

      if ($CASESENSITIVE)
      {
         if ($l =~ /$spat/)
         {
           $MATCHCOUNT++;
           ##print "   $f" . "[$c]  $l\n";
           close(IN);
           return $SUCCESS;
         }
      }
      else
      {
         if ($l =~ /$spat/i)
         {
           $MATCHCOUNT++;
           ##print "   $f" . "[$c]  $l\n";
           close(IN);
           return $SUCCESS;
         }
      }
   }

   $TOTALLINES += $c;

   # end of file
   
   print "nothing found  $f" . "\n";

   close(IN);

   return $SUCCESS;
}


#-----------------------------------------------------------------------
# process command line arguments
#-----------------------------------------------------------------------

sub ProcessCommandLineArguments
{
   my $e;                     # command line argument
   my $ee;                    # command line argument (uppercase)

   my $sp = 1;
   my $fp = 1;

   for $e (@ARGV)
   {
      $ee = $e;
      $ee =~ tr/a-z/A-Z/;

      if ($ee eq 'DEBUG')         { $DEBUG         = 1; next; }
      if ($ee eq 'VERBOSE')       { $VERBOSE       = 1; next; }
      if ($ee eq 'CASESENSITIVE') { $CASESENSITIVE = 1; next; }
      if ($ee eq 'CASE')          { $CASESENSITIVE = 1; next; }
      if ($ee eq 'SENSITIVE')     { $CASESENSITIVE = 1; next; }

      if ($sp)
      {
         $STRINGPATTERN = $e;
         $sp = 0;
         next;
      }

      if ($fp)
      {
         $FILEPATTERN = $e;
         $fp = 0;
         next;
      }

      print "\nError - Extra/Unknown parameter on command line\n";
      return $FAILURE;
   }

   return $SUCCESS;
}
