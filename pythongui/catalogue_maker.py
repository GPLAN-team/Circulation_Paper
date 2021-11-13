from turtle import width
from fpdf import FPDF
import networkx as nx
import matplotlib.pyplot as plt

pdf_w=210
pdf_h=297
pdf_w_c = 210/2
pdf_h_c = 297/2
rgb_colors = [ 	
    (123,104,238), #medium slate blue	
    (64,224,208), #turqouise
    (255,127,80), #coral
    (255,105,180), #hot pink	
    (230,230,250), #lavender
    (250,128,114), #salmon
    (152,251,152), #pale green
    (186,85,211), #medium orchid
    (176,196,222), #light steel blue
    (255,165,0), #orange
    (255,218,185), #peach puff
    (100,149,237), #corn flower blue
    ]*10
hex_colors = [
    "#7B68EE", #medium slate blue	
    "#40E0D0", #turqouise
    "#FF7F50", #coral
    "#FF69B4", #hot pink	
    "#E6E6FA", #lavender
    "#FA8072", #salmon
    "#98FB98", #pale green
    "#BA55D3", #medium orchid
    "#B0C4DE", #light steel blue
    "#FFA500", #orange
    "#FFDAB9", #peach puff
    "#6495ED", #corn flower blue
]*10

class PDF(FPDF):
    def add_border(self):
        self.set_fill_color(105,105,105) # color for outer rectangle
        self.rect(5.0, 5.0, 200.0,287.0,'DF')
        self.set_fill_color(255, 255, 255) # color for inner rectangle
        self.rect(8.0, 8.0, 194.0,282.0,'FD')
        self.set_margins(left=10, top=10, right=-10)

    def add_title(self):
        self.set_title(title= "A catalogue of floor plans")
        self.set_font('Arial', 'B', 8)
        self.multi_cell(100, 10, 'A catalogue for multiple floor plans from a given adjacency graph', 0, 1, 'C')


def save_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    nx.draw_planar(G,node_color=hex_colors[:G.number_of_nodes()], with_labels = True)
    plt.savefig('latest_adj_graph.png')
    



def draw_one_rfp(pdf: PDF, x, y, rfp_data, grid_w=100, grid_h=100, dimensioned = 0):

    # Bounding Box
    # pdf.rect( x, y, grid_w, grid_h)

    min_x = rfp_data['room_x'][0]
    min_y = rfp_data['room_y'][0]
    max_x = rfp_data['room_x'][0] + rfp_data['room_width'][0]
    max_y = rfp_data['room_y'][0] + rfp_data['room_height'][0]
    # print("min_x, max_x, min_y, max_y" , min_x, max_x, min_y, max_y)
    for each_room in range(len(rfp_data['room_x_top_left'])):

        min_x = min( min_x,  rfp_data['room_x'][each_room] )
        min_y = min( min_y,  rfp_data['room_y'][each_room] )
        max_x = min( max_x,  rfp_data['room_x'][each_room] + rfp_data['room_width'][each_room] )
        max_y = min( max_y,  rfp_data['room_y'][each_room] + rfp_data['room_height'][each_room] )

    plot_width = abs( min_x - max_x)
    plot_height = abs( min_y - max_y)
    scale = max( grid_h/plot_height, grid_w/plot_width) / 8

    # pdf.text(
    #         x + grid_w,
    #         y,
    #         txt = "Dimensions of each room" )

    # pdf.set_xy(x + grid_w - 10, y)
    if dimensioned == 1:
        pdf.text(x + grid_w, y, 'Dimensions \n')

        for each_room in range(len(rfp_data['room_x_top_left'])):
            pdf.text(x + grid_w, y + each_room * 5 + 5, 'Room ' + str(each_room) + ' : ' + str(rfp_data['room_width'][each_room]) + ' X ' + str(rfp_data['room_height'][each_room]) + '\n')

    for each_room in range(len(rfp_data['room_x_top_left'])):
        if each_room in rfp_data['extranodes']:
            continue
        if each_room in rfp_data['mergednodes']:
            rgb_colors[each_room] = rgb_colors[
                int (rfp_data['irreg_nodes'][
                    rfp_data['mergednodes'].index(each_room)
                    ])
                    ]
        pdf.set_fill_color(*rgb_colors[each_room])
        pdf.set_draw_color(0,0,0)
        pdf.rect( 
            x + scale * int(rfp_data['room_x'][each_room]) ,
            y + scale * int(rfp_data['room_y'][each_room]) , 
            scale * int(rfp_data['room_width'][each_room]) , 
            scale * int(rfp_data['room_height'][each_room]) ,
            'DF')

        if dimensioned == 1:
            if each_room not in rfp_data['mergednodes']:
                pdf.text(
                    x + scale * int(rfp_data['room_x'][each_room]) + 1,
                    y + scale * int(rfp_data['room_y'][each_room]) + 5,
                    txt = str(each_room) )

        line_width = 0.2
        pdf.set_line_width(line_width)
        pdf.set_draw_color(*rgb_colors[each_room])
        if rfp_data['room_x_bottom_left'][each_room] != rfp_data['room_x_bottom_right'][each_room]:
            pdf.line(x + scale * rfp_data['room_x_bottom_left'][each_room] + line_width, y + scale * rfp_data['room_y'][each_room], x + scale * rfp_data['room_x_bottom_right'][each_room] - line_width, y + scale * rfp_data['room_y'][each_room])
        if rfp_data['room_x_top_left'][each_room] != rfp_data['room_x_top_right'][each_room]:
            pdf.line(x + scale * rfp_data['room_x_top_left'][each_room] + line_width, y + scale * rfp_data['room_y'][each_room] + scale * rfp_data['room_height'][each_room] , x + scale * rfp_data['room_x_top_right'][each_room] - line_width, y + scale * rfp_data['room_y'][each_room] + scale * rfp_data['room_height'][each_room])
        if rfp_data['room_y_left_bottom'][each_room] != rfp_data['room_y_left_top'][each_room]:
            pdf.line( x + scale * rfp_data['room_x'][each_room],y + scale * rfp_data['room_y_left_bottom'][each_room] + line_width ,x + scale * rfp_data['room_x'][each_room], y + scale * rfp_data['room_y_left_top'][each_room] - line_width )
        if rfp_data['room_y_right_bottom'][each_room] != rfp_data['room_y_right_top'][each_room]:
            pdf.line( x + scale * rfp_data['room_x'][each_room] + scale * rfp_data['room_width'][each_room], y + scale * rfp_data['room_y_right_bottom'][each_room] + line_width , x + scale * rfp_data['room_x'][each_room] + scale * rfp_data['room_width'][each_room], y + scale * rfp_data['room_y_right_top'][each_room] - line_width)
            
        
        pdf.set_draw_color(0,0,0)



def add_dimensional_constraints(pdf : PDF, dimensional_constraints):
    [min_width,max_width,min_height,max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height] = dimensional_constraints
    if len(dimensional_constraints) != 0:
        pdf.multi_cell(100, 10, "Dimenstional Constraints \n", 0, 1, 'C')

        cons_y = pdf.y



        pdf.multi_cell(20, 10, "Room Name", 1, 1, 'C')

        pdf.y = cons_y
        pdf.x = pdf.x + 20
        pdf.multi_cell(20, 10, "Min. width", 1, 1, 'C')

        pdf.y = cons_y
        pdf.x = pdf.x + 40
        pdf.multi_cell(20, 10, "Max. Width", 1, 1, 'C')

        pdf.x = pdf.x + 60
        pdf.y = cons_y
        pdf.multi_cell(20, 10, "Min. Heigth", 1, 1, 'C')

        pdf.x = pdf.x + 80
        pdf.y = cons_y
        pdf.multi_cell(20, 10, "Max. Heigth", 1, 1, 'C')
        
        pdf.x = pdf.x + 100
        pdf.y = cons_y
        pdf.multi_cell(30, 10, "Min. Aspect Ratio", 1, 1, 'C')
        
        pdf.x = pdf.x + 130
        pdf.y = cons_y
        pdf.multi_cell(30, 10, "Max. Aspect Ratio", 1, 1, 'C')


        for room in range(len(min_width)):
            cons_y = pdf.y

            pdf.cell(20, 10, "Room" + str(room), 0, 1, 'C')
            pdf.x = pdf.x + 20
            pdf.y = cons_y

            pdf.cell(20, 10, str(min_width[room]), 0, 1, 'C')
            pdf.x = pdf.x + 40
            pdf.y = cons_y

            pdf.cell(20, 10, str(max_width[room]), 0, 1, 'C')
            pdf.x = pdf.x + 60
            pdf.y = cons_y

            pdf.cell(20, 10, str(min_height[room]), 0, 1, 'C')

            pdf.x = pdf.x + 80
            pdf.y = cons_y
            pdf.cell(20, 10, str(max_height[room]), 0, 1, 'C')

            pdf.x = pdf.x + 100
            pdf.y = cons_y
            pdf.cell(30, 10, str(min_aspect[room]), 0, 1, 'C')
            
            pdf.x = pdf.x + 130
            pdf.y = cons_y
            pdf.cell(30, 10, str(max_aspect[room]), 0, 1, 'C')


def add_home_page(pdf, edges, num_rfp, time_taken):
    pdf.add_page()
    pdf.add_border()
    pdf.add_title()
    save_graph(edges)
    pdf.multi_cell(100, 10, str( "Adjacency List: " + str(edges)), 0, 1, 'C')
    # pdf.set_y(pdf.get_y() + 10)
    x1 = pdf.get_x()
    y1 = pdf.get_y()
    pdf.image("./latest_adj_graph.png", x = x1, y = y1, w = 100, h = 100, type = 'png', link = './latest_adj_graph.png')
    pdf.set_y(pdf.get_y() + 110)
    pdf.multi_cell(100, 10, "Time taken: " + str(time_taken) + " ms", 0, 1, 'C')
    pdf.multi_cell(100, 10, "Number of floorplans: " +  str(num_rfp), 0, 1, 'C')

def generate_catalogue(edges, num_rfp, time_taken, output_data, dimensional_constraints ):
        print("[LOG] Downloading Catalogue")
        pdf = PDF() 
        add_home_page(pdf, edges, num_rfp, time_taken)
        # add_dimensional_constraints(pdf, dimensional_constraints)
        # origin = [ [75,75], [75,175], [75, 250], [175, 75], [175,175], [175, 250] ]
        origin_x = 15
        origin_y = 30

        grid_height = 20
        grid_width = 20

        grid_cols = int( (pdf_w - 50) / grid_width )
        grid_rows = int( (pdf_h - 70) / grid_height)
        # print(" cols rows" , grid_cols, grid_rows)

        rfp_no = 0
        break_while = 0
        while rfp_no < num_rfp:
            
            pdf.add_page()
            pdf.add_border()
            pdf.cell(40)
            pdf.cell(100,10, str(rfp_no) + " of " + str(num_rfp) + " Floor Plans",0,1,'C')

            for i in range(grid_rows):
                if break_while == 1:
                    break

                j = 0
                while j < grid_cols:
                    if rfp_no >= num_rfp:
                        break_while = 1
                        break

                    rfp_x = origin_x + j * (grid_width + 2)
                    rfp_y = origin_y + i * (grid_height + 2)
                    rfp_data = output_data[rfp_no]
                    draw_one_rfp(pdf, rfp_x, rfp_y, rfp_data, grid_width, grid_height)
                    rfp_no += 1
                    j += 1
        pdf.output('latest_catalogue.pdf','F')


            
def generate_catalogue_dimensioned(edges, num_rfp, time_taken, output_data, dimensional_constraints ):
        print("[LOG] Downloading Dimensioned Catalogue")
        pdf = PDF() 
        add_home_page(pdf, edges, num_rfp, time_taken)
        add_dimensional_constraints(pdf, dimensional_constraints)
        # origin = [ [75,75], [75,175], [75, 250], [175, 75], [175,175], [175, 250] ]
        origin_x = 15
        origin_y = 30

        grid_height = 50
        grid_width = 50

        grid_cols = int( (pdf_w - 30) / grid_width )
        grid_rows = int( (pdf_h - 30) / grid_height)
        # print(" cols rows" , grid_cols, grid_rows)

        rfp_no = 0
        break_while = 0
        while rfp_no < num_rfp:
            
            pdf.add_page()
            pdf.add_border()
            pdf.cell(40)
            pdf.cell(100,10, str(rfp_no) + " of " + str(num_rfp) + " Floor Plans",0,1,'C')

            for i in range(grid_rows):
                if break_while == 1:
                    break

                j = 0
                while j < grid_cols:
                    if rfp_no >= num_rfp:
                        break_while = 1
                        break

                    rfp_x = origin_x + j * (grid_width + 2)
                    rfp_y = origin_y + i * (grid_height + 2)
                    rfp_data = output_data[rfp_no]
                    draw_one_rfp(pdf, rfp_x, rfp_y, rfp_data, grid_width, grid_height, dimensioned=1)
                    rfp_no += 1
                    j += 2
                    
            

        pdf.output('latest_catalogue.pdf','F')

































# pdf = PDF() #pdf object
# pdf.add_page()
# pdf.add_border()
# pdf.add_title()
# pdf.set_fill_color(111,111,111)
# pdf.rect(50,50,50,50,'DF')

# # Set font
# # pdf.set_font('Arial', 'B', 16)
# # # Move to 8 cm to the right
# # pdf.cell(80)
# # # Centered text in a framed 20*10 mm cell and line break
# # pdf.cell(20, 10, 'Title', 1, 1, 'C')


# pdf.output('test.pdf','F')
