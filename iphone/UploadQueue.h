//
//  UploadQueue.h
//  panappticon
//
//  Created by Adam Duston on 8/2/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>


@interface UploadQueue : NSObject {
  NSOperationQueue *_operationQueue;
  NSURL *_url;
}

+ (UploadQueue*)instance;
- (void)uploadFile:(NSString*)fileName withContentType:(NSString*)contentType;

@end
