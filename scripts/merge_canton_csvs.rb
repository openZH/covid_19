#!/usr/bin/env ruby

require 'csv'

# get files
files = Dir["fallzahlen_kanton_total_csv/*.csv"]

# output array
rows = []

# read headers
header = CSV.read(files.first).first

# read all csv files
files.each do |fn|
  CSV.foreach(fn, headers: true) do |row|
    # make sure time is formatted with leading zeroes
    if row[1] =~ /(\d{1,2}):(\d{1,2})/
      row[1] = sprintf "%02d:%02d", $1.to_i, $2.to_i
    end
    rows << row[0..10]
  end
end

# sort records by date
rows.sort_by! { |x| "#{x[0]}-#{x[1]}-#{x[2]}" }

    
# output
puts header.to_csv
rows.each{ |row| puts row.to_csv }


