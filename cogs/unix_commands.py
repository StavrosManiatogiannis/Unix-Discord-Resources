import discord
from discord.ext import commands

class unix_commands(commands.Cog):

    
    
    def __init__(self, client):
        self.client = client
        self.current_path = "/"
        self.current_category = ""
        self.current_channel = ""


    
    
    
    # the depth will be 0 if we are on the root, 1 if we are in a category and 2 if we are in a channel
    def _depth_counter(path: str):
        depth = -1
        for letter in path:
            if letter == "/":
                depth += 1
        
        return depth
    
    
    
    
    # given a path it will return the category and the channel
    def _get_category_channel(path: str):
        current_word = ""
        category = ""
        channel = ""
        path = path[1:] #we omit the first character since we know it's "/"
        for letter in path:
            if letter == "/":
                category = current_word    
                current_word = ""
                continue
            else:
                current_word += letter
        
        if category == "":
            category = current_word
        else:
            channel = current_word
        return category, channel    
    
    
    
    
    
    
    
    def _is_path_valid(self, ctx, path: str):
        
        if path == '/':
            return True
        
        depth = unix_commands._depth_counter(path)
        
        if depth >= 2:
            return False

        else:
            category, channel = unix_commands._get_category_channel(path)
            try:
                category_obj= discord.utils.get(ctx.guild.categories, name = category.strip())
                if category_obj == None:
                    return False
            except:
                return False
            
            if channel != "":
                try:
                    channel_obj = None
                    channel_list = category_obj.channels
                    for channel_listed in channel_list:
                        if channel_listed.name == channel:
                            channel_obj = channel_listed
    
                    channel_check = channel_obj in category_obj.channels
                    if (channel_obj == None) or (not channel_check):
                        return False
                    else:
                        return True
                except:
                    return False
            
            # if it passes every not false check it is a valid path
            return True








   
   
    async def _is_channel_empty(channel_obj):
        # if it is not a text channel it can't have a last message id so we consider it empty 
        try:
            if channel_obj.last_message_id is None:
                return True
            else:
                return False
        
        except: 
            return True
        







    
    
    # used in rm, rmdir
    # if the channel is empty it deletes it otherwise it send the sender an error message
    async def _remove_channel(ctx, channel_obj, parameter,command):
        
        if parameter == "force":
            await channel_obj.delete()
            return None
        
        
        channel_is_empty = await unix_commands._is_channel_empty(channel_obj)
        
        if channel_is_empty:
            await channel_obj.delete()
            return None
        
        else:
            await ctx.send(f"in {command}: channel named {channel_obj.name} is not empty.")
            return -1
        

    
    
    
    
    
    #used in rmdir
    async def _remove_category(ctx, category_obj,parameters):
        
        channel_list = category_obj.channels
        delete_status = 1

        if parameters == "":
            
            if channel_list is None:
                await category_obj.delete()
                return None
            else:
                await ctx.send(f"in rmdir: The category {category_obj.name} is not empty.\nTry the option -f or the option -r if you still want to delete.")

        elif parameters == "recursive":
            for channel in channel_list:
                can_delete_channel = await unix_commands._remove_channel(ctx, channel, "recursive", "rmdir")
                if can_delete_channel is not None:
                    delete_status = None
            
            if delete_status is not None:
                await category_obj.delete()
            else:
                await ctx.send(f"in rmdir: category {category_obj.name} is not empty.\nTry using the option -r or -f.")
            return None

        elif parameters == "force":
            for channel in channel_list:
                await unix_commands._remove_channel(ctx, channel, "force", "rmdir")
            await category_obj.delete()
    




 
 
 
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is operational!")



 
 
 
 
 
 
    # sends the current working directory
    @commands.command()
    async def pwd(self, ctx):
        working_directory = f"{self.current_path}"
        await ctx.send(working_directory)




   
   
   
   
   
   
    # sends the user's username
    @commands.command()
    async def whoami(self, ctx):
        await ctx.send(ctx.author.name)



  
  
  
  
  
  
    # turns the bot down
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def shutdown(self, ctx):
        goodbye_message = f"I will remember this {ctx.author.mention}."
        print(f"SHUTTING DOWN! The user {ctx.author.name} has ordered this bot to shutdown.")
        await ctx.send(goodbye_message)
        await self.client.close()



    
   
   
   
   
   
   
   
   
   
   
    # prints all the channels inside the current directory
    # options:
    #                 -a lists the hidden channels too (the ones whose name begins with ".")                              
    #                 -l formats the output into a list
    @commands.command()
    async def ls(self, ctx, *arg):
        channel_list = []
        channel_names = ""
        parameter_l = 0
        parameter_a = 0
        
        if self.current_channel != "":
            await ctx.send(" ")
        
        
        if self.current_path == "/":
            channel_list = ctx.guild.categories 
        else:
            category_name = self.current_category.strip()
            category_obj = discord.utils.get(ctx.guild.categories, name = category_name)
            channel_list = category_obj.channels
        
        
        try:
            if arg[0][0] == "-":
                if "l" in arg[0]:
                    parameter_l = 1
                if "a" in arg[0]:
                    parameter_a = 1 
        except:
            pass

        
        parameter_l_character = " "
        if parameter_l == 1:
            parameter_l_character = "\n"
        
        for channel in channel_list:
            if channel.name[0] == "." and parameter_a == 0:
                continue
            else:
                channel_names +=  channel.name + parameter_l_character
        

        await ctx.send(channel_names)



  
  
  
  
  
  
  
  
    # the command to navigate around the files
    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def cd(self, ctx, *arg):
        print(arg)
        
        
        error_message = "in cd: no such channel"
        path_specified = ""
        new_path = ""

        try:
            first_character = arg[0][0] #if the first character of the given path is / then we know it's an absolute path otherwise it's a relative path
        except:
            await ctx.send("in cd: directory was not specified.")
            return None
        
        

        for i in arg:
            path_specified += i + " "
        path_specified = path_specified.strip()
        
        # if the path is absolute
        if first_character == "/" :
            new_path = path_specified.strip()
            if self._is_path_valid(ctx, new_path):
                self.current_path = new_path
                try:
                    self.current_category, self.current_channel = unix_commands._get_category_channel(new_path)
                except:
                    self.current_category = new_path[1:].strip()

                return None
            else:
                await ctx.send(error_message)
        
        # if the path is relative
        else:
            if path_specified == ".":
                return None
            if path_specified == "..":
                if self.current_channel != "":
                    self.current_path = f"/{self.current_category}"
                    self.current_channel = ""
                    return None
                else:
                    self.current_path = "/"
                    self.category = ""
                    return None
            
            if self.current_path != "/":
                new_path = self.current_path.strip() + "/" + path_specified.strip()
            else:
                new_path = "/" + path_specified.strip()
            
            if self._is_path_valid(ctx, new_path):
                self.current_path = new_path
                self.current_category, self.current_channel = unix_commands._get_category_channel(new_path)
                return None
            else:
                await ctx.send(error_message)





  
  
  
  
  
  
  
    # makes a channel inside a category channel
    # options (only one can be used): 
    #           -t : creates a text channel
    #           -v : creates a voice channel
    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def mk(self, ctx, *arg):
        new_name = ""
        forbidden_character_list = ["/"]
        channel_type = "text" # the default option for channel is text channel
        
        # you cant make a channel inside a non category channel
        if self.current_path == "/":
            await ctx.send("Error! You cannot make a non-category channel outsid a category channel.")
            return None
        
        
        if self.current_channel != "":
            await ctx.send("Error! You cannot make a non-category channel inside a non-category channel.")
            return None
        
        
        try:
            parameters = arg[0]
            if parameters[0] =="-":
                if parameters[1] == "t":
                    channel_type = "text"
                elif parameters[1] == "v":
                    channel_type = "voice"
                # we no longer need the first entry of the argument
                arg = arg[1:]
        except:
            await ctx.send("Error! You did not enter the name of the channel.")
            return None
        
        
        try:
        
            
            for i in arg:
                if not (i in forbidden_character_list) :
                    new_name += i + " "
                else:
                    await ctx.send("Not a valid channel name.")
                    return None
            
            new_name = new_name.strip()
        
        except:
            await ctx.send("Error! You did not enter the name of the channel.")
            return None


        new_channel_path = self.current_path.strip() + "/" +new_name.strip()
        if self._is_path_valid(ctx, new_channel_path):
            await ctx.send("Error! A channel with that name exists in this category.")
            return None

        category_obj = category_obj= discord.utils.get(ctx.guild.categories, name = self.current_category.strip())
        #create the new channel 
        if channel_type == "text":
            await ctx.guild.create_text_channel(new_name, category = category_obj)
            return None
        
        if channel_type == "voice":
            await ctx.guild.create_voice_channel(new_name, category = category_obj)
            return None

        return None


  
  
  
  
  
  
  
  
    #deletes the specified non-category channel
    #options:
    #           -f  deletes non empty channels
    @commands.command()
    @commands.has_permissions(manage_channels = True, read_message_history = True)
    async def rm(self, ctx, *arg):
        
        # if no option is used then the rm command will not delete non-empty channels
        remove_parameter = "none"

        if self.current_path == "/":
            await ctx.send("in rm: you can only remove non-category channels.")
            return None
        
        if self.current_channel != "":
            await ctx.send("You can't use rm to remove the inside of a channel")
            return None
        
        try:
            print("in rm the user has inputted ",arg)
            parameter = arg[0]
            if parameter[0] == "-":
                if parameter[1] == "f":
                    remove_parameter = "force"
                # if element 0 was a parameter we start from element 1 
                arg = arg[1:]
        except:
            await ctx.send("in rm: No channel specified")
        
        
        channel_name = ""
        for i in arg:
            channel_name += i + " "
        
        channel_name = channel_name.strip()
        new_path_remove = self.current_path.strip() + "/" + channel_name
        print("in rm user has specified the channel ",channel_name)
        
        if not self._is_path_valid(ctx, new_path_remove):
            await ctx.send("There is no channel with that name.")
            return None
        print("in rm made it before declaring the objects")
        
        
        category_obj = discord.utils.get(ctx.guild.categories, name = self.current_category.strip())
        channel_list = category_obj.channels
        channel_obj = None
        for channel in channel_list:
            if channel.name == channel_name:
                channel_obj = channel
                break
        
        unix_commands._remove_channel(ctx, channel_obj, remove_parameter, "rm")





  
  
  
  
  
  
    # makes a category channel
    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def mkdir(self, ctx, *arg):

        if self.current_path != "/":
            await ctx.send("in mkdir: You can only make a channel category in root.")    
            return None
        
        new_category_name = ""
        forbidden_character_list = ["/"]
        
        try:
            for i in arg:
                new_category_name += i + " "
            
            new_category_name = new_category_name.strip()
            
            # check whether the name is allowed
            for letter in new_category_name:
                
                if letter in forbidden_character_list:
                    await ctx.send("in mkdir: not a valid name")
                    return None
        
        
        except:
            await ctx.send("in mkdir: Category name was not specified.")
            return None

        # checks whether the category already exists
        created_path = "/" + new_category_name
        if self._is_path_valid(ctx, created_path):
            await ctx.send(f"in mkdir: {new_category_name} category already exists.")
            return None
        
        await ctx.guild.create_category(new_category_name)



   
   
   
   
   
   
   
   
   
    # removes a category channel:
    # options:
    #           -r    deletes every non-empty channel inside category
    #           -f    deletes category and every channel in it regardless of emptyness
    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def rmdir(self, ctx, *arg):
        current_command = "rmdir"
        
        remove_directory_parameter = ""
        
        if self.current_path != "/":
            await ctx.send("in rmdir: You can only remove categories with this command. Try rm instead.")
        
        
        try:
            for i in arg:
                parameter = arg[0]
                if parameter[0] == "-":
                    if parameter[1] == "f":
                        remove_directory_parameter = "force"
                    elif parameter[1] == "r":
                        remove_directory_parameter = "recursive"
                    arg = arg[1:]
        except:
            await ctx.send("in rmdir: you have to specify which category to remove.")
            return None


        category_name = ""
        for i in arg:
            category_name += i + " "
        category_name = category_name.strip()

        category_obj = discord.utils.get(ctx.guild.categories, name = category_name)

        await unix_commands._remove_category(ctx, category_obj, remove_directory_parameter)







    # moves a non-category channel from one category to another or renames a category channel
    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def mv(self, ctx, *arg):
        

        if self.current_channel != "":
            await ctx.send("in mv: there are no channels here")
            return None
        
        try:
            initial_path = arg[0]
            final_path = arg[1]
        except:
            await ctx.send("in mv: no file was specified.")

        
        
        if initial_path[0] != "/":
            initial_path = self.current_path.strip() + "/" + initial_path.strip()
        
        if final_path[0] != "/":
            final_path = self.current_path.strip() + "/" + final_path.strip()

        print(f"initial path | {initial_path}")
        print(f"final path | {final_path}")
    
        
        if not (self._is_path_valid(ctx, initial_path)):
            await ctx.send(f"in mv: could not find {initial_path}")
            return None
        
        if self._is_path_valid(ctx, final_path):
            await ctx.send(f"in mv: {final_path} already exists")
            return None

        print("path is valid is not the problem")
        initial_depth = unix_commands._depth_counter(initial_path)
        final_depth = unix_commands._depth_counter(final_path)
        
        if (initial_depth != final_depth):
            await ctx.send("in mv: cannot convert channel in category and vice versa.")
            return None

        print("before getting initial_category")
        initial_category, initial_channel = unix_commands._get_category_channel(initial_path)
        final_category, final_channel = unix_commands._get_category_channel(final_path)
        
        print("made it before category_obj")
        initial_category_obj = discord.utils.get(ctx.guild.categories, name = initial_category.strip())
        print("made it to the initial_category_obj")
        initial_category_channels = initial_category_obj.channels
        
        initial_channel_obj = None
        for channel in initial_category_channels:
            if channel.name == initial_channel:
                initial_channel_obj = channel
                break
    
        print("If i do not show up you know whats up")
        
        final_category_obj = discord.utils.get(ctx.guild.categories, name = final_category.strip())
        #final_channel_obj = discord.utils.get(category = final_category_obj, name = final_channel.strip())
        
        if final_channel != "":
            if not (final_category_obj in ctx.guild.categories):
                await ctx.send(f"in mv: category {final_category} could not be found.") 
                return None
            await initial_channel_obj.edit(category = final_category_obj, name = final_channel.strip())
        

        else:
            await initial_category_obj.edit(name = final_channel.strip())


async def setup(client):
    await client.add_cog(unix_commands(client))
