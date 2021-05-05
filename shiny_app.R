

library(shiny)
library(shinydashboard)
library(leaflet)
library(sf)
library(ggplot2)
library(htmltools)
library(scales)


settl_sim <- st_read("selected_settlements_MG_simed.shp",stringsAsFactors = F) %>% st_as_sf()
hosp_sim <- st_read("selected_hospital_sites_MG_simed_thin.shp",stringsAsFactors = F) %>% st_as_sf() 
gh_admin <- st_read("gh_country_adm_0.shp",stringsAsFactors = F) %>% st_as_sf()
pv_potential <- read.csv("weekly_pv_potential_weekC.csv") %>% as.data.frame()
pv_potential_clr <- read.csv("weekly_pv_clrsky_potential_weekC.csv") %>% as.data.frame()



up_logo   <- "https://next.rl-institut.de/s/kSTBYf2RSJLMctH/preview"
rli_logo  <- "https://next.rl-institut.de/s/sEPj2NbZjMAsFS3/preview"
enershelf_logo <- "https://next.rl-institut.de/s/DfGdRYXcwrwjFK4/preview"
space_im  <- "https://next.rl-institut.de/s/AbTzxCpSWTMWg2J/preview"
ccbysa_im <- "https://next.rl-institut.de/s/rwb4f3Y79pTDxeX/preview"
hosp_icon <- "https://next.rl-institut.de/s/ws8tNnPagSnf6X9/preview"

hospIcon <- makeIcon(
  iconUrl = hosp_icon,
  iconWidth = 8, iconHeight = 8,
  iconAnchorX = 0, iconAnchorY = 0,
)

ui <- dashboardPage(skin = "blue",
                    dashboardHeader(title = "GHANA PV Mini Grid Simulations", titleWidth = 450),
                    dashboardSidebar(disable = TRUE),
                    dashboardBody(
                      tags$head(tags$style(HTML('
        .skin-blue .main-header .logo {
          background-color: #3c8dbc;
        }
        .skin-blue .main-header .logo:hover {
          background-color: #3c8dbc;
        }
      '))),
                      fluidRow(
                        box(width = 8, #height = 90,
                            strong("SOLAR PV MINI GRID SIMULATIONS FOR SELECTED HOSPITAL AND COMMUNITY CLUSTERS IN GHANA") %>% h3()
                        ),
                        box(width = 4,height = 90,
                            img(src = enershelf_logo, height=60,align = "right"),
                            img(src = space_im, height=15,align = "right"),
                            img(src = up_logo, height=60,align = "right"),
                            img(src = space_im, height=15,align = "right"),
                            img(src = rli_logo, height=60,align = "right")), #align = "right"
                        box(leafletOutput("map", height = 600),width = 7),
                        valueBoxOutput("hosp_name",width = 3),
                        valueBoxOutput("hosp_demand",width= 2),
                        box(plotOutput("plot3", height = 300),width = 5),
                        valueBoxOutput("inst_cap",width = 3),
                        valueBoxOutput("inst_lcoe",width = 2),
                        valueBoxOutput("FI_cost",width = 5),
                        
                        box(width = 10,
                            "The data displayed on this platform depicts results of research done on the", 
                            "Assessment of Photovoltaic Micro-grids Potential in Supporting Health Facilities", 
                            "and Communities in Ghana, by Arnold Wasike, as part of Master thesis Deliverables.", 
                            "This was done in conjunction with", 
                            tags$a(href="https://reiner-lemoine-institut.de/", "Reiner Lemoine Institute, "),
                            tags$a(href="https://www.uni-potsdam.de/en/geo/", "University of Potsdam, "), "and",
                            tags$a(href="https://enershelf.de/", "Enershelf."),
                            br(),
                            "Derived data and results are shared under the CC-BY-SA license. They can be accessed", 
                            "by writing to", 
                            tags$a(href="mailto:Arnold.wasike@rl-institut.de", "Arnold.wasike@rl-institut.de. "),
                            "Selection of hospitals and clusters for", 
                            "study were done by a multi criteria method, detailed in the thesis, and have no socioeconomic", 
                            "or political groundings. The boarders depicted are also not our endorsement of national boundaries,", 
                            "but an approximation of national extents."
                        ),
                        box(width = 2,
                            img(src = ccbysa_im, height=60,align = "right"))
                      )
                    )
)

# Define server logic ----
server <- function(input, output) {
  output$map <- renderLeaflet({
    leaflet() %>% 
      addProviderTiles("OpenStreetMap.Mapnik", group = "OSM") %>% #OpenStreetMap.Mapnik ,NASAGIBS.ViirsEarthAtNight2012
      addProviderTiles("Esri.WorldImagery", group = "Esri World Imagery") %>%
      addProviderTiles("NASAGIBS.ViirsEarthAtNight2012", group = "NASA VIIRS Night") %>%
      addPolygons(data = gh_admin, 
                  weight = 3,
                  color = "#83c1ffff",
                  opacity = 0.6,
                  fillOpacity = 0) %>% 
      addMarkers(data = hosp_sim, 
                 icon = hospIcon,
                 options = pathOptions(clickable = FALSE)) %>%
      addPolygons(data = settl_sim, 
                  color = "#ffc337ff",
                  opacity = 1,
                  fillOpacity = 0,
                  label = ~htmlEscape(join_Facil),
                  labelOptions = labelOptions(textsize = "15px"),
                  layerId = ~FID) %>% 
      addLayersControl(
        baseGroups = c("OSM", "Esri World Imagery","NASA VIIRS Night"),
        options = layersControlOptions(collapsed = T)
      )
  })
  observe({
    event <- input$map_shape_click
    output$plot3 <- renderPlot({
      ev_id <- event$id
      if (is.null(ev_id)) {
        ev_id =662
        al_v <-0 
      }else{
        al_v <-1 
      }
      is.null(ev_id)
      
      pv_station <- subset(pv_potential,fid == ev_id) #range 90 - 240
      pv_station$fid <- NULL
      pv_station <- pv_station %>% t() %>% as.array() %>% as.double() %>%  as.data.frame() 
      pv_station$PV_Watts <- pv_station$.
      pv_station$Week <- seq(1:nrow(pv_station)) 
      pv_station$. <- NULL
      
      pv_st_clr <- subset(pv_potential_clr,fid == ev_id) #range 213 - 291
      pv_st_clr$fid <- NULL
      pv_st_clr <- pv_st_clr %>% t() %>% as.array() %>% as.double() %>%  as.data.frame() 
      pv_st_clr$Cl_Sky <- pv_st_clr$.
      pv_st_clr$Week <- seq(1:nrow(pv_st_clr)) 
      pv_st_clr$. <- NULL
      
      colors <- c("PV potential" = "#3b85d3ff", "Clear sky" = "#ffc337ff")
      ggplot() + #pv_station, aes(x=Week, y=PV_Watts)) +
        geom_step(data=pv_st_clr, mapping=aes(x=Week, y=Cl_Sky,color ="Clear sky"),size=1.2,alpha=al_v) +
        geom_step(data=pv_station, mapping=aes(x=Week, y=PV_Watts,color ="PV potential"),size=1.2,alpha=al_v) +
        expand_limits(y = c(90,300))+ ylim(90, 300) + xlab("Week") + ylab("PV Potential (W)") + 
        labs(color = "Legend") +scale_color_manual(values = colors) + 
        theme(legend.title = element_blank(),
              legend.position = c(1, 1),
              legend.background = element_blank(),
              legend.justification = c("right", "top"))
    })
    output$hosp_name <- renderValueBox({
      hosp_name_val <- paste0(settl_sim$selected_h[settl_sim$FID == event$id])
      valueBox(
        value = tags$p(hosp_name_val, style = "font-size: 20px;"),
        "Health Facility",
        color = "blue"
      )
    })
    output$hosp_demand <- renderValueBox({
      hosp_demand_val <- dollar_format(prefix = "",suffix = " KWh",largest_with_cents = 1e+09)(c(settl_sim$selected13[settl_sim$FID == event$id]))
      valueBox(
        value = tags$p(hosp_demand_val, style = "font-size: 20px;"),
        "Demand", 
        color = "yellow"
      )
    })
    output$inst_cap <- renderValueBox({
      inst_cap_val <- dollar_format(prefix = "",suffix = " KWP",largest_with_cents = 1e+09)(c(settl_sim$selected14[settl_sim$FID == event$id])) # %>% round(digits=2) %>% paste0(" KWP")
      valueBox(
        value = tags$p(inst_cap_val, style = "font-size: 20px;"),
        "Installed Capacity Needed",
        color = "blue"
      )
    })
    output$inst_lcoe <- renderValueBox({
      inst_lcoe_val <- dollar_format(prefix = "",suffix = " $/KWh",largest_with_cents = 1e+09)(c(settl_sim$selected15[settl_sim$FID == event$id]))
      valueBox(
        value = tags$p(inst_lcoe_val, style = "font-size: 20px;"),
        "LCOE",
        color = "yellow"
      )
    })
    output$FI_cost <- renderValueBox({
      FI_hosp <- dollar_format(prefix = "$ ",suffix = "",largest_with_cents = 1e+09)(c(settl_sim$selected_8[settl_sim$FID == event$id]))
      FI_comm <- dollar_format(prefix = "$ ",suffix = "",largest_with_cents = 1e+09)(c(settl_sim$selected_4[settl_sim$FID == event$id]))
      FI_cost_val <- paste0(FI_hosp," || ",FI_comm)
      valueBox(
        value = tags$p(FI_cost_val, style = "font-size: 30px;"),
        "First Investment Cost for Hospital and Hospital-Cluster Combination",
        color = "navy"
      )
    })
  })
}

# Run the app ----
shinyApp(ui = ui, server = server)







