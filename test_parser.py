from thin_line_grid import parse_input_file

polyline_sets = parse_input_file()
for polyline_set in polyline_sets:
    print(f"Polyline Set: {polyline_set.name}, Color: {polyline_set.display_colour}")
    for idx, polyline in enumerate(polyline_set.polylines):
        print(f"  Polyline {idx+1}: {polyline}")