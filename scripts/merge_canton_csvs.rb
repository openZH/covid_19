#!/usr/bin/env ruby

require 'csv'

files = Dir["fallzahlen_kanton_total_csv/*.csv"]

puts CSV.read(files.first).first.to_csv

files.each do |fn|
  CSV.foreach(fn, headers: true) do |row|
    puts row[0..10].to_csv
  end
end
    



