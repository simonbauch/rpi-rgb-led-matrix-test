# distutils: language = c++

from libcpp cimport bool
from libc.stdint cimport uint8_t, uint32_t, uintptr_t
from PIL import Image
import cython

cdef class Canvas:
    cdef cppinc.Canvas* __getCanvas(self) except +:
        raise Exception("Not implemented")

    def SetImage(self, image, int offset_x = 0, int offset_y = 0, unsafe=True):
        if (image.mode != "RGB"):
            raise Exception("Currently, only RGB mode is supported for SetImage(). Please create images with mode 'RGB' or convert first with image = image.convert('RGB'). Pull requests to support more modes natively are also welcome :)")

        if unsafe:
            #In unsafe mode we directly access the underlying PIL image array
            #in cython, which is considered unsafe pointer accecss,
            #however it's super fast and seems to work fine
            #https://groups.google.com/forum/#!topic/cython-users/Dc1ft5W6KM4
            img_width, img_height = image.size
            self.SetPixelsPillow(offset_x, offset_y, img_width, img_height, image)
        else:
            # First implementation of a SetImage(). OPTIMIZE_ME: A more native
            # implementation that directly reads the buffer and calls the underlying
            # C functions can certainly be faster.
            img_width, img_height = image.size
            pixels = image.load()
            for x in range(max(0, -offset_x), min(img_width, self.width - offset_x)):
                for y in range(max(0, -offset_y), min(img_height, self.height - offset_y)):
                    (r, g, b) = pixels[x, y]
                    self.SetPixel(x + offset_x, y + offset_y, r, g, b)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def SetPixelsPillow(self, int xstart, int ystart, int width, int height, image):
        cdef cppinc.FrameCanvas* my_canvas = <cppinc.FrameCanvas*>self.__getCanvas()
        cdef int frame_width = my_canvas.width()
        cdef int frame_height = my_canvas.height()
        cdef int row, col
        cdef uint8_t r, g, b
        cdef uint32_t **image_ptr
        cdef uint32_t pixel
        image.load()
        ptr_tmp = dict(image.im.unsafe_ptrs)['image32']
        image_ptr = (<uint32_t **>(<uintptr_t>ptr_tmp))

        for col in range(max(0, -xstart), min(width, frame_width - xstart)):
            for row in range(max(0, -ystart), min(height, frame_height - ystart)):
                pixel = image_ptr[row][col]
                r = (pixel ) & 0xFF
                g = (pixel >> 8) & 0xFF
                b = (pixel >> 16) & 0xFF
                my_canvas.SetPixel(xstart+col, ystart+row, r, g, b)

    def SetPixelsCrosshair(self, int x1, int y1, uint32_t color1):
        cdef cppinc.FrameCanvas* my_canvas = <cppinc.FrameCanvas*>self.__getCanvas()
        cdef int frame_width = my_canvas.width()
        cdef int frame_height = my_canvas.height()
        cdef int row = 0
        cdef int col = 0
        cdef uint8_t r, g, b
        x1=x1-1
        y1=y1-1
        r = (color1 ) & 0xFF
        g = (color1 >> 8) & 0xFF
        b = (color1 >> 16) & 0xFF
        for col in range(0, frame_width,1):
            for row in range(0, frame_height,1):
                    if col==x1 or row==y1:
                        my_canvas.SetPixel(col, row, r, g, b)

    def SetPixelstwoCrosshair(self, int x1, int y1, int x2, int y2, uint32_t color1, uint32_t color2):
        cdef cppinc.FrameCanvas* my_canvas = <cppinc.FrameCanvas*>self.__getCanvas()
        cdef int frame_width = my_canvas.width()
        cdef int frame_height = my_canvas.height()
        cdef int row = 0
        cdef int col = 0
        cdef uint8_t r1, g1, b1, r2, g2, b2
        x1=x1-1
        y1=y1-1
        x2=x2-1
        y2=y2-1
        r1 = (color1 ) & 0xFF
        g1 = (color1 >> 8) & 0xFF
        b1 = (color1 >> 16) & 0xFF
        r2 = (color2 ) & 0xFF
        g2 = (color2 >> 8) & 0xFF
        b2 = (color2 >> 16) & 0xFF
        for col in range(0, frame_width,1):
            for row in range(0, frame_height,1):
                    if col==x1 or row==y1:
                        my_canvas.SetPixel(col, row, r1, g1, b1)
                    if col==x2 or row==y2:
                        if x1!=x2 and y1!=y2:
                            my_canvas.SetPixel(col, row, r2, g2, b2)
    
    def SetPixelsthreeCrosshair(self, int x1, int y1, int x2, int y2, int x3, int y3, uint32_t color1, uint32_t color2, uint32_t color3):
        cdef cppinc.FrameCanvas* my_canvas = <cppinc.FrameCanvas*>self.__getCanvas()
        cdef int frame_width = my_canvas.width()
        cdef int frame_height = my_canvas.height()
        cdef int row = 0
        cdef int col = 0
        cdef uint8_t r1, g1, b1, r2, g2, b2, r3, g3, b3
        x1=x1-1
        y1=y1-1
        x2=x2-1
        y2=y2-1
        x3=x3-1
        y3=y3-1
        r1 = (color1 ) & 0xFF
        g1 = (color1 >> 8) & 0xFF
        b1 = (color1 >> 16) & 0xFF
        r2 = (color2 ) & 0xFF
        g2 = (color2 >> 8) & 0xFF
        b2 = (color2 >> 16) & 0xFF
        r3 = (color3 ) & 0xFF
        g3 = (color3 >> 8) & 0xFF
        b3 = (color3 >> 16) & 0xFF
        for col in range(0, frame_width,1):
            for row in range(0, frame_height,1):
                    if col==x1 or row==y1:
                        my_canvas.SetPixel(col, row, r1, g1, b1)
                    if col==x2 or row==y2:
                        #if x1!=x2 and y1!=y2:
                        my_canvas.SetPixel(col, row, r2, g2, b2)
                    if col==x3 or row==y3:
                        #if x1!=x3 and x2!=x3 and y1!=y3 and y2!=y3:
                        my_canvas.SetPixel(col, row, r3, g3, b3)
    def SetPixelsthreeCrosshairsmall(self, int x1, int y1, int x2, int y2, int x3, int y3, uint32_t color1, uint32_t color2, uint32_t color3, int lenght):
        cdef cppinc.FrameCanvas* my_canvas = <cppinc.FrameCanvas*>self.__getCanvas()
        cdef int frame_width = my_canvas.width()
        cdef int frame_height = my_canvas.height()
        cdef int row = 0
        cdef int col = 0
        cdef uint8_t r1, g1, b1, r2, g2, b2, r3, g3, b3
        x1=x1-1
        y1=y1-1
        x2=x2-1
        y2=y2-1
        x3=x3-1
        y3=y3-1
        r1 = (color1 ) & 0xFF
        g1 = (color1 >> 8) & 0xFF
        b1 = (color1 >> 16) & 0xFF
        r2 = (color2 ) & 0xFF
        g2 = (color2 >> 8) & 0xFF
        b2 = (color2 >> 16) & 0xFF
        r3 = (color3 ) & 0xFF
        g3 = (color3 >> 8) & 0xFF
        b3 = (color3 >> 16) & 0xFF
        for col in range(0, frame_width,1):
            for row in range(0, frame_height,1):                        
                    if ((y1 > (row - lenght)) and (y1 < (row + lenght))) and ((x1 > (col - lenght)) and (x1 < (col + lenght))):
                        if row == y1 or col ==x1:    
                            my_canvas.SetPixel(col, row, r1, g1, b1)
                    if ((y2 > (row - lenght)) and (y2 < (row + lenght))) and ((x2 > (col - lenght)) and (x2 < (col + lenght))):
                        if row == y2 or col ==x2:    
                            my_canvas.SetPixel(col, row, r2, g2, b2)
                    if ((y3 > (row - lenght)) and (y3 < (row + lenght))) and ((x3 > (col - lenght)) and (x3 < (col + lenght))):
                        if row == y3 or col ==x3:    
                            my_canvas.SetPixel(col, row, r3, g3, b3)
                    
    
           
            

cdef class FrameCanvas(Canvas):
    def __dealloc__(self):
        if <void*>self.__canvas != NULL:
            self.__canvas = NULL

    cdef cppinc.Canvas* __getCanvas(self) except *:
        if <void*>self.__canvas != NULL:
            return self.__canvas
        raise Exception("Canvas was destroyed or not initialized, you cannot use this object anymore")

    def Fill(self, uint8_t red, uint8_t green, uint8_t blue):
        (<cppinc.FrameCanvas*>self.__getCanvas()).Fill(red, green, blue)

    def Clear(self):
        (<cppinc.FrameCanvas*>self.__getCanvas()).Clear()

    def SetPixel(self, int x, int y, uint8_t red, uint8_t green, uint8_t blue):
        (<cppinc.FrameCanvas*>self.__getCanvas()).SetPixel(x, y, red, green, blue)


    property width:
        def __get__(self): return (<cppinc.FrameCanvas*>self.__getCanvas()).width()

    property height:
        def __get__(self): return (<cppinc.FrameCanvas*>self.__getCanvas()).height()

    property pwmBits:
        def __get__(self): return (<cppinc.FrameCanvas*>self.__getCanvas()).pwmbits()
        def __set__(self, pwmBits): (<cppinc.FrameCanvas*>self.__getCanvas()).SetPWMBits(pwmBits)

    property brightness:
        def __get__(self): return (<cppinc.FrameCanvas*>self.__getCanvas()).brightness()
        def __set__(self, val): (<cppinc.FrameCanvas*>self.__getCanvas()).SetBrightness(val)


cdef class RGBMatrixOptions:
    def __cinit__(self):
        self.__options = cppinc.Options()
        self.__runtime_options = cppinc.RuntimeOptions()

    # RGBMatrix::Options properties
    property hardware_mapping:
        def __get__(self): return self.__options.hardware_mapping
        def __set__(self, value):
            self.__py_encoded_hardware_mapping = value.encode('utf-8')
            self.__options.hardware_mapping = self.__py_encoded_hardware_mapping

    property rows:
        def __get__(self): return self.__options.rows
        def __set__(self, uint8_t value): self.__options.rows = value

    property cols:
        def __get__(self): return self.__options.cols
        def __set__(self, uint32_t value): self.__options.cols = value

    property chain_length:
        def __get__(self): return self.__options.chain_length
        def __set__(self, uint8_t value): self.__options.chain_length = value

    property parallel:
        def __get__(self): return self.__options.parallel
        def __set__(self, uint8_t value): self.__options.parallel = value

    property pwm_bits:
        def __get__(self): return self.__options.pwm_bits
        def __set__(self, uint8_t value): self.__options.pwm_bits = value

    property pwm_lsb_nanoseconds:
        def __get__(self): return self.__options.pwm_lsb_nanoseconds
        def __set__(self, uint32_t value): self.__options.pwm_lsb_nanoseconds = value

    property brightness:
        def __get__(self): return self.__options.brightness
        def __set__(self, uint8_t value): self.__options.brightness = value

    property scan_mode:
        def __get__(self): return self.__options.scan_mode
        def __set__(self, uint8_t value): self.__options.scan_mode = value

    property multiplexing:
        def __get__(self): return self.__options.multiplexing
        def __set__(self, uint8_t value): self.__options.multiplexing = value

    property row_address_type:
        def __get__(self): return self.__options.row_address_type
        def __set__(self, uint8_t value): self.__options.row_address_type = value

    property disable_hardware_pulsing:
        def __get__(self): return self.__options.disable_hardware_pulsing
        def __set__(self, value): self.__options.disable_hardware_pulsing = value

    property show_refresh_rate:
        def __get__(self): return self.__options.show_refresh_rate
        def __set__(self, value): self.__options.show_refresh_rate = value

    property inverse_colors:
        def __get__(self): return self.__options.inverse_colors
        def __set__(self, value): self.__options.inverse_colors = value

    property led_rgb_sequence:
        def __get__(self): return self.__options.led_rgb_sequence
        def __set__(self, value):
            self.__py_encoded_led_rgb_sequence = value.encode('utf-8')
            self.__options.led_rgb_sequence = self.__py_encoded_led_rgb_sequence

    property pixel_mapper_config:
        def __get__(self): return self.__options.pixel_mapper_config
        def __set__(self, value):
            self.__py_encoded_pixel_mapper_config = value.encode('utf-8')
            self.__options.pixel_mapper_config = self.__py_encoded_pixel_mapper_config

    property panel_type:
        def __get__(self): return self.__options.panel_type
        def __set__(self, value):
            self.__py_encoded_panel_type = value.encode('utf-8')
            self.__options.panel_type = self.__py_encoded_panel_type

    property pwm_dither_bits:
        def __get__(self): return self.__options.pwm_dither_bits
        def __set__(self, uint8_t value): self.__options.pwm_dither_bits = value

    property limit_refresh_rate_hz:
        def __get__(self): return self.__options.limit_refresh_rate_hz
        def __set__(self, value): self.__options.limit_refresh_rate_hz = value


    # RuntimeOptions properties

    property gpio_slowdown:
        def __get__(self): return self.__runtime_options.gpio_slowdown
        def __set__(self, uint8_t value): self.__runtime_options.gpio_slowdown = value

    property daemon:
        def __get__(self): return self.__runtime_options.daemon
        def __set__(self, uint8_t value): self.__runtime_options.daemon = value

    property drop_privileges:
        def __get__(self): return self.__runtime_options.drop_privileges
        def __set__(self, uint8_t value): self.__runtime_options.drop_privileges = value

cdef class RGBMatrix(Canvas):
    def __cinit__(self, int rows = 0, int chains = 0, int parallel = 0,
        RGBMatrixOptions options = None):

        # If RGBMatrixOptions not provided, create defaults and set any optional
        # parameters supplied
        if options == None:
            options = RGBMatrixOptions()

        if rows > 0:
            options.rows = rows
        if chains > 0:
            options.chain_length = chains
        if parallel > 0:
            options.parallel = parallel

        self.__matrix = cppinc.CreateMatrixFromOptions(options.__options,
            options.__runtime_options)

    def __dealloc__(self):
        self.__matrix.Clear()
        del self.__matrix

    cdef cppinc.Canvas* __getCanvas(self) except *:
        if <void*>self.__matrix != NULL:
            return self.__matrix
        raise Exception("Canvas was destroyed or not initialized, you cannot use this object anymore")

    def Fill(self, uint8_t red, uint8_t green, uint8_t blue):
        self.__matrix.Fill(red, green, blue)

    def SetPixel(self, int x, int y, uint8_t red, uint8_t green, uint8_t blue):
        self.__matrix.SetPixel(x, y, red, green, blue)

    def Clear(self):
        self.__matrix.Clear()

    def CreateFrameCanvas(self):
        return __createFrameCanvas(self.__matrix.CreateFrameCanvas())

    # The optional "framerate_fraction" parameter allows to choose which
    # multiple of the global frame-count to use. So it slows down your animation
    # to an exact integer fraction of the refresh rate.
    # Default is 1, so immediately next available frame.
    # (Say you have 140Hz refresh rate, then a value of 5 would give you an
    # 28Hz animation, nicely locked to the refresh-rate).
    # If you combine this with RGBMatrixOptions.limit_refresh_rate_hz you can create
    # time-correct animations.
    def SwapOnVSync(self, FrameCanvas newFrame, uint8_t framerate_fraction = 1):
        return __createFrameCanvas(self.__matrix.SwapOnVSync(newFrame.__canvas, framerate_fraction))

    property luminanceCorrect:
        def __get__(self): return self.__matrix.luminance_correct()
        def __set__(self, luminanceCorrect): self.__matrix.set_luminance_correct(luminanceCorrect)

    property pwmBits:
        def __get__(self): return self.__matrix.pwmbits()
        def __set__(self, pwmBits): self.__matrix.SetPWMBits(pwmBits)

    property brightness:
        def __get__(self): return self.__matrix.brightness()
        def __set__(self, brightness): self.__matrix.SetBrightness(brightness)

    property height:
        def __get__(self): return self.__matrix.height()

    property width:
        def __get__(self): return self.__matrix.width()

cdef __createFrameCanvas(cppinc.FrameCanvas* newCanvas):
    canvas = FrameCanvas()
    canvas.__canvas = newCanvas
    return canvas

# Local Variables:
# mode: python
# End:
