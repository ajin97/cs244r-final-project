require 'aviglitch'
require 'spreadsheet'

a = AviGlitch.open 'dataset/6.avi'
all_frames = []
a.frames.each_with_index do |f, i|
  all_frames.push(i)
end
q = a.frames[0, 0]

# Read in a spreadsheet that details
# which frames to keep and make a new
# video keeping exactly those frames.
d = []
Spreadsheet.open('dataset/frames_kept_pct_drop.XLS') do |book|
  book.worksheet('Sheet1').each do |row|
    d.push(row[17])
  end
end
puts d

i = -1
400.times do
  i = i + 1
  if d.include? i
    x = a.frames[all_frames[i], 1]
    q.concat(x * 1)
  end
end
o = AviGlitch.open q
o.output 'dataset/30pctvid6.avi'
