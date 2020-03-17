The project consists of 2 workers and a web part.  

The first worker receives data from the ticket service  
`python manage.py scraper`

The second worker does the normalization of the downloaded data.  
`python manage.py normalize_data`


The web part allows you to make some requests:  
`GET /api/events` - get all events  
`GET /api/events?event_name={search_event_name}` search for events by name  
`GET /api/events?ticket_cost={ticket_cost}` search for events by cost (price_min<=ticket_cost<=price_max)  

Event update:
`PUT /api/events/{event.id}`  
```json
{
     "event_name": "test3",  
     "promoter_name": "test_name3"
}
```  
