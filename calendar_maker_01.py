# -*- coding: utf-8 -*-
import svgwrite, math, numpy

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

# PARAMETERS
textAngleShift = -0.0018 # in radians
canvasSize = (500,707)
dayFontFamily = "PT Sans"
dayFontSize = "1.8pt"
rainbowGradient =		[[  0,  0,  0,239,255,255,255,  0,  0],
				 		 [254,248,246,194,  0,  0,  0,211,254],
				 		 [255,193,  0,  0,  0,210,255,255,255]]
rainbowGradientPoints = [math.pi*2/8*0,\
						math.pi*2/8*1,\
						math.pi*2/8*2,\
						math.pi*2/8*3,\
						math.pi*2/8*4,\
						math.pi*2/8*5,\
						math.pi*2/8*6,\
						math.pi*2/8*7,\
						math.pi*2/8*8 \
						]
#print rainbowGradientPoints
#rainbowGradient =  [[  0,255,  0],
					#[255,  0,  0],
					#[  0,  0,255]]
#rainbowGradientPoints = [0, math.pi, math.pi*2]

# ConvertedParameters
k = 1.2
R_seasons_beg =  k*canvasSize[0]*0.1
R_mounthes_beg = k*canvasSize[0]*0.25
R_weeks_beg  =   k*canvasSize[0]*0.3
R_days_beg   =   k*canvasSize[0]*0.305
R_days_end   =   k*canvasSize[0]*0.307
R_dates =        k*canvasSize[0]*0.312
mid = canvasSize[0]/2.0, canvasSize[1]/2.0

# Make a year circle

#calculate day circles
#calculate week circles
#calculate mounth circles
dayAngle = math.pi*2/365
weekAngle = dayAngle*7
mounthes = [u'января',\
			u'февраля',\
			u'марта',\
			u'апреля',\
			u'мая',\
			u'июня',\
			u'июля',\
			u'августа',\
			u'сентября',\
			u'октября',\
			u'ноября',\
			u'декабря'\
			]
#mounthes = [u'Января',\
			#u'Февраля',\
			#u'Марта',\
			#u'Апреля',\
			#u'Мая',\
			#u'Июня',\
			#u'Июля',\
			#u'Августа',\
			#u'Сентября',\
			#u'Октября',\
			#u'Ноября',\
			#u'Декабря'\
			#]
mounthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
yearDays = ["%d %s"%(i+1, mounthes[index]) \
#yearDays = ["%d"%(i+1) \
				  for index, m in enumerate(mounthDays) \
				  for i in range(m)]
allFirstDates = [ 0 if i!=0 else \
				  1 if (index+1)%3!=0 else \
				  2 \
				  for index, m in enumerate(mounthDays) \
				  for i in range(m)]
mounthAngles = [d*dayAngle for d in mounthDays]


dwg = svgwrite.Drawing('calendar.svg', profile='tiny', width="%dpx"%(canvasSize[0]), height="%dpx"%(canvasSize[1]))


textGroup = dwg.g(font_family=dayFontFamily, \
	 font_size=dayFontSize,\
	 text_anchor="start" )
	 #text_anchor="end" ) )
dayLineGroup = dwg.g(stroke_width=0.4, fill='none')
weekLineGroup = dwg.g(stroke_width=0.2, fill='none')
mounthesLineGroup = dwg.g(stroke_width=0.1, fill='none')
seasonsLineGroup = dwg.g(stroke_width=0.05, fill='none')

#draw text
for index, angle in enumerate(frange(0,math.pi*2,dayAngle)):
	colorTuple = (int(numpy.interp(angle, rainbowGradientPoints, rainbowGradient[0])), \
		 int(numpy.interp(angle, rainbowGradientPoints, rainbowGradient[1])), \
		 int(numpy.interp(angle, rainbowGradientPoints, rainbowGradient[2])))
	color = "rgb%s"%(str(colorTuple))
	sinus =   math.sin(angle)
	cosinus = math.cos(angle)
	# Draw a week segment
	if (index-5)%7 == 0:
		weekLineGroup.add (dwg.line( (mid[0]-R_weeks_beg*sinus,mid[1]+R_weeks_beg*cosinus), \
			 (mid[0]-R_days_beg *sinus,mid[1]+R_days_beg *cosinus), \
			 stroke=color) )
	# Draw a mounth+season segments
	if allFirstDates[index]!=0:
		mounthesLineGroup.add (dwg.line( (mid[0]-R_mounthes_beg*sinus,mid[1]+R_mounthes_beg*cosinus), \
			 (mid[0]-R_weeks_beg *sinus,mid[1]+R_weeks_beg*cosinus), \
			 stroke=color) )
		# Draw a season
		if allFirstDates[index]==2:
			seasonsLineGroup.add (dwg.line( (mid[0]-R_seasons_beg*sinus,mid[1]+R_seasons_beg*cosinus), \
				 (mid[0]-R_mounthes_beg *sinus,mid[1]+R_mounthes_beg*cosinus), \
				 stroke=color) )
	# Draw a day
	dayLineGroup.add (dwg.line( (mid[0]-R_days_beg*sinus,mid[1]+R_days_beg*cosinus), \
		 (mid[0]-R_days_end *sinus,mid[1]+R_days_end *cosinus), \
		 stroke=color
		 ) )
	# Draw a day name
	#wordGroup = dwg.g()
	wordGroup = dwg.g(transform="rotate(%f, %f, %f) translate(%f,0)" \
		%(math.degrees(angle+dayAngle+textAngleShift)+90, mid[0], mid[1], +R_dates))
	#wordGroup = dwg.g(transform="rotate(%f, %f, %f) translate(%f,0)" \
		#%(math.degrees(angle)-90, mid[0], mid[1], -R))
	wordGroup.add( dwg.text( '%s'%(yearDays[index]), \
		insert=mid ))
	textGroup.add(wordGroup)

	
	sinus_end =   math.sin(angle+dayAngle)
	cosinus_end = math.cos(angle+dayAngle)
	# draw circles segments
	# days
	dayLineGroup.add( dwg.line( (mid[0]-R_days_beg*sinus,	 mid[1]+R_days_beg*cosinus), \
								(mid[0]-R_days_beg*sinus_end,mid[1]+R_days_beg*cosinus_end), \
								stroke=color ) )
	weekLineGroup.add( dwg.line((mid[0]-R_weeks_beg*sinus,	  mid[1]+R_weeks_beg*cosinus), \
								(mid[0]-R_weeks_beg*sinus_end,mid[1]+R_weeks_beg*cosinus_end), \
								stroke=color ) )
	mounthesLineGroup.add( dwg.line((mid[0]-R_mounthes_beg*sinus,	  mid[1]+R_mounthes_beg*cosinus), \
								(mid[0]-R_mounthes_beg*sinus_end,mid[1]+R_mounthes_beg*cosinus_end), \
								stroke=color ) )
	seasonsLineGroup.add( dwg.line((mid[0]-R_seasons_beg*sinus,	  mid[1]+R_seasons_beg*cosinus), \
								(mid[0]-R_seasons_beg*sinus_end,mid[1]+R_seasons_beg*cosinus_end), \
								stroke=color ) )


	# weeks
	# mounthes
	# seasons

#dayLineGroup.add( dwg.circle(center=mid, r=R_days_beg, stroke='black' ) )
#weekLineGroup.add( dwg.circle(center=mid, r=R_weeks_beg, stroke='black' ) )
#mounthesLineGroup.add( dwg.circle(center=mid, r=R_mounthes_beg, stroke='black' ) )
#seasonsLineGroup.add( dwg.circle(center=mid, r=R_seasons_beg, stroke='black') )

dwg.add(textGroup)
dwg.add(dayLineGroup)
dwg.add(weekLineGroup)
dwg.add(mounthesLineGroup)
dwg.add(seasonsLineGroup)

dwg.add(dwg.rect((0, 0), canvasSize, stroke='gray', fill="none"))
dwg.add(dwg.text("2014", insert=(mid[0],mid[1]+4), text_anchor="middle", font_family="PT Serif", font_size="10pt"))
dwg.save()
