//
//  PanappticonDatabase.m
//  Panappticon
//
//  Created by Adam Duston on 8/1/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import "PanappticonDatabase.h"
#import "Utilities.h"

#import <UIKit/UIKit.h>

static PanappticonDatabase *_instance = nil;

@interface PanappticonDatabase()

- (void)addOperation:(NSOperation*)operation;
- (void)saveTagImpl:(NSArray*)args;
- (void)flushToURLImpl:(NSString*)url;

@end


@implementation PanappticonDatabase

- (PanappticonDatabase*)init {
  if (self = [super init]) {
    _operationQueue = [[NSOperationQueue alloc] init];
    _operationQueue.maxConcurrentOperationCount = 1;
  }
  return self;
}

+ (PanappticonDatabase*)instance {
  @synchronized (self) {
    if (_instance == nil)
      _instance = [[PanappticonDatabase alloc] init];
  }
  return _instance;
}

+ (void)saveTag:(NSString*)tagName 
         forApp:(NSString*)appName 
     forSession:(NSString*)session 
 withScreenshot:(UIImage*)screenshot {
  NSArray *args = [NSArray arrayWithObjects:tagName, appName, session, 
                   (screenshot == nil ? 
                    (NSObject*)[NSNull null] : 
                    (NSObject*)screenshot), 
                   nil];
  NSOperation *operation = [[NSInvocationOperation alloc] 
                            initWithTarget:self 
                            selector:@selector(saveTagImpl:) 
                            object:args];
  [[PanappticonDatabase instance] addOperation:operation];
  [operation release];
}

+ (void)flushToURL:(NSString*)url {
  NSOperation *operation = [[NSInvocationOperation alloc]
                            initWithTarget:self 
                            selector:@selector(flushToURLImpl:) 
                            object:url];
  [[PanappticonDatabase instance] addOperation:operation];
  [operation release];
}

#pragma mark -
#pragma mark Private Methods

- (void)addOperation:(NSOperation*)operation {
  [_operationQueue addOperation:operation];
}

- (void)saveTagImpl:(NSArray*)args {
  NSString *tagName = [args objectAtIndex:0];
  NSString *appName = [args objectAtIndex:1];
  NSString *sessionID = [args objectAtIndex:2];
  UIImage *screenshot = 
  [args objectAtIndex:3] == [NSNull null] ? 
  nil : [args objectAtIndex:3];
  NSString* screenshotString = @"";
  if (screenshot != nil)
    screenshotString = [Utilities base64Encode:UIImagePNGRepresentation(screenshot)];
  
}

- (void)flushToURLImpl:(NSString*)url {
  
}

@end
