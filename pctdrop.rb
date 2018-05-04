require 'aviglitch'

a = AviGlitch.open '../streaming/dataset/5.avi'
all_frames = []
d = []
a.frames.each_with_index do |f, i|
  d.push(i) if f.is_deltaframe?     # Collecting P/B frame indices.
  all_frames.push(i)
end
puts d.length
puts all_frames.length
q = a.frames[0, 1]

# Loop through all frames:
# keep all I frames and
# keep each P/B frame with the prescribed
# probability
i = -1
100.times do
  i = i + 1
  if d.include? i
    if rand(100) < 10
      next
    end
  end
  puts i
  x = a.frames[all_frames[i], 1]
  q.concat(x * 1)
end
o = AviGlitch.open q
o.output '5vid10pctdrop.avi'
