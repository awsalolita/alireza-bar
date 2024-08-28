# Route calculator

```python
client = boto3.client(
    'location'
)
route = client.calculate_route(
    CalculatorName='connected-ambulances',
    DepartNow=False,
    IncludeLegGeometry=True,
    DeparturePosition=[
        json_data['data']['longitude'], json_data['data']['latitude']
    ],
    DestinationPosition=[
        json_data['data']['destination_longitude'], json_data['data']['destination_latitude']
    ]
)
eta = round(route['Summary']['DurationSeconds']/60)
line_string = route['Legs'][0]['Geometry']['LineString']
```