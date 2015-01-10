sunday = "monday"; monday = "sunday"
t = {sunday = "monday", [sunday] = monday}
print(t.sunday, t[sunday], t[t.sunday])
-- prints "monday sunday sunday"

-- [[ TODO: explain ]]
a = {x=10, y=20}
-- TODO: is equivalent to
a = {}; a.x=10; a.y=20
-- now look at this
w = {x=0, y=0, label="console"}
x = {math.sin(0), math.sin(1), math.sin(2)}
w[1] = "another field"	-- add key 1 to table w with value "another field"
x.f = w					-- add key "f" to table x with the contents of table w
print(w["x"])			-- prints 0
print(w[1])				-- prints "another field"
print(x.f[1])			-- prints "another field" (key 1 in w)
w.x = nil				-- TODO: remove key x from w
-- now this
polyline = {
	color="blue", 
	thickness=2,
	npoints=4,
	this={x=0, y=0},			-- polyline[1]
	{x=-10, y=0},		-- polyline[2]
	{x=-10, y=1},		-- polyline[3]
	{x=0, y=1}			-- polyline[4]
}
--[[ TODO: Check this block... ]]
print(polyline["this"].x)	-- FIXME: prints -10 --
print(polyline[4].y)	-- prints 1
print(polyline["color"])		-- referencing "color" key
print(polyline["npoints"])		-- referencing "npoints" key

-- note that this:
a = {x=10, y=20}
-- is equivalent to this:
a = {["x"]=10, ["y"]=20}
-- and that this:
b = {"r", "g", "b"}
-- is equivalent to:
b = {[1]="r", [2]="g", [3]="b"}

