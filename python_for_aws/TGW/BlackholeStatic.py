import boto3
from botocore.exceptions import ClientError

def create_transit_gateway_route_with_blackhole(tgw_route_table_id, destination_cidr):

    ec2 = boto3.client('ec2')

    
    result = ec2.create_transit_gateway_route(
        TransitGatewayRouteTableId=tgw_route_table_id,
        DestinationCidrBlock=destination_cidr,
        Blackhole=True)






tgw_route_table_id = 'tgw-rtb-04d006097099f4ce8'  # Replace with your transit gateway route table ID
destination_cidr = '10.0.0.0/24'  # Replace with your destination CIDR

create_transit_gateway_route_with_blackhole(tgw_route_table_id, destination_cidr)