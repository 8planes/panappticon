//
//  UploadQueue.m
//  panappticon
//
//  Created by Adam Duston on 8/2/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import "UploadQueue.h"
#import "ASIFormDataRequest.h"

static UploadQueue *_instance = nil;

@interface UploadQueue()

- (void)uploadFileImpl:(NSArray*)args;

@end

@implementation UploadQueue
@synthesize url = _url;

- (UploadQueue*)init {
  if (self == [super init]) {
    _operationQueue = [[NSOperationQueue alloc] init];
    _operationQueue.maxConcurrentOperationCount = 1;
  }
  return self;
}

+ (UploadQueue*)instance {
  @synchronized (self) {
    if (!_instance)
      _instance = [[UploadQueue alloc] init];
  }
  return _instance;
}

- (void)uploadFile:(NSString*)fileName withContentType:(NSString*)contentType {
  NSOperation *operation = [[NSInvocationOperation alloc]
                            initWithTarget:self selector:@selector(uploadFileImpl:) 
                            object:[NSArray arrayWithObjects:fileName, contentType, nil]];
  [_operationQueue addOperation:operation];
  [operation release];
}

#pragma mark -
#pragma mark Private Methods

// called from operation queue only.
- (void)uploadFileImpl:(NSArray*)args {
  NSString* fileName = [args objectAtIndex:0];
  NSString* lastComponent = [fileName lastPathComponent];
  NSString* contentType = [args objectAtIndex:1];
  
  NSFileManager *fileManager = [NSFileManager defaultManager];
  if (![fileManager fileExistsAtPath:fileName])
    return;

  ASIFormDataRequest *request = [ASIFormDataRequest requestWithURL:_url];
  [request setFile:fileName withFileName:lastComponent andContentType:contentType forKey:@"file"];
  [request startSynchronous];
  NSError *error = [request error];
  if (!error)
    [fileManager removeItemAtPath:fileName error:nil];
}

@end
