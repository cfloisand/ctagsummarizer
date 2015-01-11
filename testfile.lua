-- Lua test file for ctag.

sunday = "monday"; monday = "sunday"
t = {sunday = "monday", [sunday] = monday}
print(t.sunday, t[sunday], t[t.sunday])
-- prints "monday sunday sunday"

--[[ TODO: This is a todo item in Lua. ]]
a = {x=10, y=20}
-- TODO: Review Lua.. I totally forget how to program in this.
a = {}; a.x=10; a.y=20
-- Just a useless comment
w = {x=0, y=0, label="console"}
x = {math.sin(0), math.sin(1), math.sin(2)}
w[1] = "another field"	-- add key 1 to table w with value "another field"
x.f = w					-- add key "f" to table x with the contents of table w
print(w["x"])			-- prints 0
print(w[1])				-- prints "another field"
print(x.f[1])			-- prints "another field" (key 1 in w)
w.x = nil				-- TODO: remove key x from w

-- FIXME: Note that this:
a = {x=10, y=20}
-- is equivalent to this:
a = {["x"]=10, ["y"]=20}
-- and that this:
b = {"r", "g", "b"}
--[[ FIXME: ...is equivalent to: ]]
b = {[1]="r", [2]="g", [3]="b"}

