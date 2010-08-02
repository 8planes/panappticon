//
//  Utilities.m
//  Panopticon
//
//  Created by Adam Duston on 8/1/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import "Utilities.h"
#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>

static char encodingTable[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

@implementation Utilities

+ (NSString*)encode:(const uint8_t*) input length:(NSInteger) length {
  // Thanks to Cyrus Najmabadi
  // From http://www.cocoadev.com/index.pl?BaseSixtyFour
  NSMutableData* data = [NSMutableData dataWithLength:((length + 2) / 3) * 4];
  uint8_t* output = (uint8_t*)data.mutableBytes;
  
  for (NSInteger i = 0; i < length; i += 3) {
    NSInteger value = 0;
    for (NSInteger j = i; j < (i + 3); j++) {
      value <<= 8;
      
      if (j < length) {
        value |= (0xFF & input[j]);
      }
    }
    
    NSInteger index = (i / 3) * 4;
    output[index + 0] =                    encodingTable[(value >> 18) & 0x3F];
    output[index + 1] =                    encodingTable[(value >> 12) & 0x3F];
    output[index + 2] = (i + 1) < length ? encodingTable[(value >> 6)  & 0x3F] : '=';
    output[index + 3] = (i + 2) < length ? encodingTable[(value >> 0)  & 0x3F] : '=';
  }
  
  return [[[NSString alloc] initWithData:data
                                encoding:NSASCIIStringEncoding] autorelease];
}

+ (NSString*)randomString {
  CFUUIDRef theUUID = CFUUIDCreate(NULL);
  CFStringRef stringUUID = CFUUIDCreateString(NULL, theUUID);
  CFRelease(theUUID);
  return [(NSString *)stringUUID autorelease];
}

+ (NSString*)base64Encode:(NSData*)data {
  return [self encode:(const uint8_t*)data.bytes length:data.length];
}

+ (UIImage*)screenshot {
  // Copied from http://developer.apple.com/iphone/library/qa/qa2010/qa1703.html
  // TODO: Figure out how to show a UIActivityIndicatorView or buttonless 
  // UIAlertView while this is running (if necessary).
  
  // Create a graphics context with the target size
  // On iOS 4 and later, use UIGraphicsBeginImageContextWithOptions to take the scale into consideration
  // On iOS prior to 4, fall back to use UIGraphicsBeginImageContext
  CGSize imageSize = [[UIScreen mainScreen] bounds].size;
  if (NULL != UIGraphicsBeginImageContextWithOptions)
    UIGraphicsBeginImageContextWithOptions(imageSize, NO, 0);
  else
    UIGraphicsBeginImageContext(imageSize);
  
  CGContextRef context = UIGraphicsGetCurrentContext();
  
  // Iterate over every window from back to front
  for (UIWindow *window in [[UIApplication sharedApplication] windows]) {
    if (![window respondsToSelector:@selector(screen)] || 
        [window screen] == [UIScreen mainScreen]) {
      // -renderInContext: renders in the coordinate space of the layer,
      // so we must first apply the layer's geometry to the graphics context
      CGContextSaveGState(context);
      // Center the context around the window's anchor point
      CGContextTranslateCTM(context, [window center].x, [window center].y);
      // Apply the window's transform about the anchor point
      CGContextConcatCTM(context, [window transform]);
      // Offset by the portion of the bounds left of and above the anchor point
      CGContextTranslateCTM(context,
                            -[window bounds].size.width * [[window layer] anchorPoint].x,
                            -[window bounds].size.height * [[window layer] anchorPoint].y);
      
      // Render the layer hierarchy to the current context
      [[window layer] renderInContext:context];
      
      // Restore the context
      CGContextRestoreGState(context);
    }
  }
  
  // Retrieve the screenshot image
  UIImage *image = UIGraphicsGetImageFromCurrentImageContext();
  
  UIGraphicsEndImageContext();
  
  return image;
}

@end
