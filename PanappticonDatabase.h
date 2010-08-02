//
//  PanappticonDatabase.h
//  Panappticon
//
//  Created by Adam Duston on 8/1/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface PanappticonDatabase : NSObject {
  // can be accessed by any thread
  NSOperationQueue *_operationQueue;
}

+ (PanappticonDatabase*)instance;

+ (void)saveTag:(NSString*)tagName 
         forApp:(NSString*)appName 
     forSession:(NSString*)session 
 withScreenshot:(UIImage*)screenshot;

+ (void)flushToURL:(NSString*)url;

@end
