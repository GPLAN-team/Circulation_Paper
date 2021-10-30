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
    
        
def generate_catalogue(edges, num_rfp, time_taken, output_data ):
        print("[LOG] Downloading Catalogue")
        pdf = PDF() 
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
        idx = 6
        origin = [ [75,75], [75,175], [75, 250], [175, 75], [175,175], [175, 250] ]
        print(output_data[0])

        for rfp in range(num_rfp):
            if idx == 6:
                pdf.add_page()
                pdf.add_border()
                idx = 0
                pdf.cell(40)
                pdf.cell(100,10, str(rfp) + " of " + str(num_rfp) + " Floor Plans",0,1,'C')
            
            origin_x = origin[idx][0] - 50
            origin_y = origin[idx][1] - 50
            # pdf.multi_cell(origin_x, origin_y, str(output_data[i]), 0, 1, 'C')
            scale = 10
            # print(pdf_colors)
            for each_room in range(len(output_data[rfp]['room_x_top_left'])):
                if each_room in output_data[rfp]['extranodes']:
                    continue
                if each_room in output_data[rfp]['mergednodes']:
                    rgb_colors[each_room] = rgb_colors[
                        int (output_data[rfp]['irreg_nodes'][
                            output_data[rfp]['mergednodes'].index(each_room)
                            ])
                            ]
                pdf.set_fill_color(*rgb_colors[each_room])
                pdf.set_draw_color(0,0,0)
                pdf.rect( 
                    origin_x + scale * int(output_data[rfp]['room_x'][each_room]) ,
                    origin_y + scale * int(output_data[rfp]['room_y'][each_room]) , 
                    scale * int(output_data[rfp]['room_width'][each_room]) * 1, 
                    scale * int(output_data[rfp]['room_height'][each_room])* 1,
                    'DF')

                if each_room not in output_data[rfp]['mergednodes']:
                    pdf.text(
                        origin_x + scale * int(output_data[rfp]['room_x'][each_room])  + 5,
                        origin_y + scale * int(output_data[rfp]['room_y'][each_room])  + 5,
                        txt = str(each_room) )

                line_width = 0.2
                pdf.set_line_width(line_width)
                pdf.set_draw_color(*rgb_colors[each_room])
                if output_data[rfp]['room_x_bottom_left'][each_room] != output_data[rfp]['room_x_bottom_right'][each_room]:
                    pdf.line(origin_x + scale * output_data[rfp]['room_x_bottom_left'][each_room] + line_width, origin_y + scale * output_data[rfp]['room_y'][each_room], origin_x + scale * output_data[rfp]['room_x_bottom_right'][each_room] - line_width, origin_y + scale * output_data[rfp]['room_y'][each_room])
                if output_data[rfp]['room_x_top_left'][each_room] != output_data[rfp]['room_x_top_right'][each_room]:
                    pdf.line(origin_x + scale * output_data[rfp]['room_x_top_left'][each_room] + line_width, origin_y + scale * output_data[rfp]['room_y'][each_room] + scale * output_data[rfp]['room_height'][each_room] , origin_x + scale * output_data[rfp]['room_x_top_right'][each_room] - line_width, origin_y + scale * output_data[rfp]['room_y'][each_room] + scale * output_data[rfp]['room_height'][each_room])
                if output_data[rfp]['room_y_left_bottom'][each_room] != output_data[rfp]['room_y_left_top'][each_room]:
                    pdf.line( origin_x + scale * output_data[rfp]['room_x'][each_room],origin_y + scale * output_data[rfp]['room_y_left_bottom'][each_room] + line_width ,origin_x + scale * output_data[rfp]['room_x'][each_room], origin_y + scale * output_data[rfp]['room_y_left_top'][each_room] - line_width )
                if output_data[rfp]['room_y_right_bottom'][each_room] != output_data[rfp]['room_y_right_top'][each_room]:
                    pdf.line( origin_x + scale * output_data[rfp]['room_x'][each_room] + scale * output_data[rfp]['room_width'][each_room], origin_y + scale * output_data[rfp]['room_y_right_bottom'][each_room] + line_width , origin_x + scale * output_data[rfp]['room_x'][each_room] + scale * output_data[rfp]['room_width'][each_room], origin_y + scale * output_data[rfp]['room_y_right_top'][each_room] - line_width)
                    
                
                pdf.set_draw_color(0,0,0)
                

                    
            # print("i = ", i)
            # print(" output_data[i]['room_x_top_left']" , output_data[i])
            idx+=1
            

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
