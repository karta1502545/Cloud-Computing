import json
import boto3

def clear_table(table):
    tableScan = table.scan()
    with table.batch_writer() as batch:
        for item in tableScan['Items']:
            batch.delete_item(
                Key={
                    'source': item['source'],
                    'destination': item['destination']
                }    
            )
        
    

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    table = dynamodb.Table('Graph')
    clear_table(table)
    
    edges = event["graph"].split(',')
    g = {}
    for edge in edges:
        source, dest = edge.split("->")
        if source in g:
            g[source].append(dest)
        else:
            g[source] = [dest]
    try:
        # for each node, run bfs then put data into DynamoDB
        for source in g:
            board = bfs(g, source)
            for dest in board.keys():
                table.put_item(
                    Item = {'source': source,
                            'destination': dest,
                            'distance': board[dest]
                    }
                )
            
        return {
            'statusCode': 200,
            'body': json.dumps('Succesfully inserted the graph!')
        }
    except Exception as e:
        print("Error: ", e)
        return {
                'statusCode': 400,
                'body': json.dumps('Error saving the graph!')
        }
    
    
# return distance from start to all the other nodes
def bfs(g, start):
    q = [(start, 0)] # node, distance
    board = {start: 0}
    while q:
        nowNode, nowDist = q.pop(0)
        if nowNode in g:
            for neighbor in g[nowNode]:
                if neighbor not in board:
                    board[neighbor] = nowDist + 1
                    q.append((neighbor, nowDist + 1))
                else:
                    pass
    return board
